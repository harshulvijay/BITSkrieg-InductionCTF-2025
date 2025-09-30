import qsharp
import re
import sys
from typing import List, Dict, Tuple

class QuantumCTFVerifier:
    def __init__(self):
        self.test_cases = []
        self.setup_test_cases()
    
    def setup_test_cases(self):
        self.framework_code = """
        operation IdentityOp(q : Qubit) : Unit is Adj + Ctl {
        }
        
        operation MinusIdentityOp(q : Qubit) : Unit is Adj + Ctl {
            R1(3.14159265359, q);
        }
        
        operation PrepZero(q : Qubit) : Unit { 
        }
        
        operation PrepOne(q : Qubit) : Unit { 
            X(q); 
        }
        
        operation PrepPlus(q : Qubit) : Unit { 
            H(q); 
        }
        
        operation PrepMinus(q : Qubit) : Unit { 
            X(q); 
            H(q); 
        }
        
        operation TestSingleRun(
            userOp : ((Qubit => Unit is Adj + Ctl, Qubit) => Int),
            testOp : (Qubit => Unit is Adj + Ctl),
            prepState : (Qubit => Unit)
        ) : Int {
            use testQubit = Qubit();
            prepState(testQubit);
            let result = userOp(testOp, testQubit);
            Reset(testQubit);
            return result;
        }
        
        operation RunMultipleTests(
            userOp : ((Qubit => Unit is Adj + Ctl, Qubit) => Int),
            testOp : (Qubit => Unit is Adj + Ctl),
            trials : Int
        ) : Int[] {
            mutable results = [];
            for i in 1..trials {
                use testQubit = Qubit();
                PrepPlus(testQubit);
                let result = userOp(testOp, testQubit);
                set results += [result];
                Reset(testQubit);
            }
            return results;
        }
        """
    
    def extract_operation(self, qsharp_code: str) -> str:
        code = re.sub(r'//.*?\n', '\n', qsharp_code)
        pattern = r'operation\s+DistinguishUOneUMinusOne.*?^\s*}'
        match = re.search(pattern, code, re.MULTILINE | re.DOTALL)
        if not match:
            raise ValueError("DistinguishUOneUMinusOne operation not found")
        return match.group(0)
    
    def validate_signature(self, operation_code: str) -> bool:
        has_correct_name = bool(re.search(r'operation\s+DistinguishUOneUMinusOne', operation_code))
        has_u_param = bool(re.search(r'u\s*:\s*Qubit\s*=>\s*Unit\s+is\s+Adj\s*\+\s*Ctl', operation_code))
        has_psi_param = bool(re.search(r'psi\s*:\s*Qubit', operation_code))
        has_int_return = bool(re.search(r':\s*Int', operation_code))
        return has_correct_name and has_u_param and has_psi_param and has_int_return
    
    def check_required_elements(self, operation_code: str) -> Dict[str, bool]:
        checks = {
            'uses_auxiliary_qubit': bool(re.search(r'use\s+\w+\s*=\s*Qubit\(\)', operation_code)),
            'applies_hadamard': len(re.findall(r'H\s*\(', operation_code)) >= 2,
            'uses_controlled': bool(re.search(r'Controlled\s+u\s*\(', operation_code)),
            'measures_qubit': bool(re.search(r'M\s*\(', operation_code)),
            'resets_qubit': bool(re.search(r'Reset\s*\(', operation_code)),
            'returns_correctly': bool(re.search(r'return.*?(Zero|result).*?\?.*?0.*?\|.*?1', operation_code))
        }
        return checks
    
    def run_functional_tests(self, user_operation: str) -> Dict[str, any]:
        full_code = self.framework_code + "\n\n" + user_operation
        try:
            print("\n   Compiling Q# code...")
            qsharp.eval(full_code)
            print("   ✅ Code compiled successfully")
            test_results = {}
            print("   Running identity tests...")
            identity_results = []
            for i in range(10):
                try:
                    result = qsharp.eval("TestSingleRun(DistinguishUOneUMinusOne, IdentityOp, PrepZero)")
                    identity_results.append(result)
                except Exception as e:
                    identity_results.append(0)
            test_results['identity_results'] = identity_results
            identity_avg = sum(identity_results) / len(identity_results)
            identity_success = identity_avg < 0.3
            print("   Running differential tests...")
            z_results = []
            for i in range(10):
                try:
                    result = qsharp.eval("TestSingleRun(DistinguishUOneUMinusOne, Z, PrepPlus)")
                    z_results.append(result)
                except Exception as e:
                    z_results.append(1)
            test_results['z_on_plus_results'] = z_results
            z_avg = sum(z_results) / len(z_results)
            print("   Running X gate tests...")
            x_results = []
            for i in range(10):
                try:
                    result = qsharp.eval("TestSingleRun(DistinguishUOneUMinusOne, X, PrepZero)")
                    x_results.append(result)
                except Exception as e:
                    x_results.append(1)
            test_results['x_results'] = x_results
            x_avg = sum(x_results) / len(x_results)
            shows_discrimination = abs(identity_avg - z_avg) > 0.2 or abs(identity_avg - x_avg) > 0.2
            test_results['functional_score'] = {
                'identity_avg': identity_avg,
                'z_avg': z_avg,
                'x_avg': x_avg,
                'identity_correct': identity_success,
                'shows_discrimination': shows_discrimination,
                'algorithm_works': identity_success and shows_discrimination
            }
            print(f"   📊 Identity avg: {identity_avg:.2f}, Z avg: {z_avg:.2f}, X avg: {x_avg:.2f}")
            return test_results
        except Exception as e:
            print(f"   ❌ Compilation/Runtime error: {e}")
            return {
                'error': str(e), 
                'functional_score': {
                    'identity_correct': False, 
                    'shows_discrimination': False,
                    'algorithm_works': False
                }
            }
    
    def verify_solution(self, qsharp_code: str) -> Dict[str, any]:
        print("=" * 60)
        print("🔍 QUANTUM CTF SOLUTION VERIFIER")
        print("=" * 60)
        verification_results = {
            'valid_submission': False,
            'signature_correct': False,
            'required_elements': {},
            'functional_tests': {},
            'score': 0,
            'feedback': []
        }
        try:
            print("\n📝 Step 1: Extracting operation...")
            operation_code = self.extract_operation(qsharp_code)
            print("✅ Operation found")
            print("🔍 Step 2: Validating signature...")
            signature_valid = self.validate_signature(operation_code)
            verification_results['signature_correct'] = signature_valid
            if signature_valid:
                print("✅ Signature is correct")
                verification_results['feedback'].append("\n✅ Function signature is correct")
            else:
                print("❌ Invalid signature")
                verification_results['feedback'].append("❌ Function signature is incorrect")
                return verification_results
            print("🔧 Step 3: Checking required quantum elements...")
            element_checks = self.check_required_elements(operation_code)
            verification_results['required_elements'] = element_checks
            missing_elements = [k for k, v in element_checks.items() if not v]
            if not missing_elements:
                print("✅ All required elements present")
                verification_results['feedback'].append("✅ All required quantum operations present")
            else:
                print(f"❌ Missing elements: {missing_elements}")
                verification_results['feedback'].append(f"❌ Missing required elements: {missing_elements}")
            print("🧪 Step 4: Running functional tests...")
            functional_results = self.run_functional_tests(operation_code)
            verification_results['functional_tests'] = functional_results
            if 'error' in functional_results:
                verification_results['feedback'].append(f"❌ Runtime error occurred during testing")
            score = 0
            if signature_valid: 
                score += 25
            element_score = sum(element_checks.values()) / len(element_checks) * 25
            score += int(element_score)
            if 'error' not in functional_results:
                func_score = functional_results.get('functional_score', {})
                if func_score.get('identity_correct', False):
                    score += 25
                if func_score.get('shows_discrimination', False):
                    score += 25
            verification_results['score'] = score
            verification_results['valid_submission'] = score >= 97
            if verification_results['valid_submission']:
                print(f"\n🎉 SOLUTION ACCEPTED! Score: {score}/100")
                print("Flag: InductionCTF{qu4n7um_c0mpu73r5_d0_b3_fun}")
                verification_results['feedback'].append("🎉 Solution implements quantum phase distinguisher correctly!")
            else:
                print(f"\n❌ SOLUTION NEEDS IMPROVEMENT. Score: {score}/100 (Need 97+ to pass)")
                verification_results['feedback'].append("❌ Solution needs improvement to pass")
            return verification_results
        except Exception as e:
            verification_results['feedback'].append(f"❌ Error processing submission: {str(e)}")
            print(f"❌ Error: {str(e)}")
            return verification_results

def main():
    if len(sys.argv) != 2:
        sys.exit(1)
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as f:
            qsharp_code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    verifier = QuantumCTFVerifier()
    results = verifier.verify_solution(qsharp_code)
    for feedback in results['feedback']:
        print(feedback)
    print(f"\nFinal Score: {results['score']}/100")
    print(f"Status: {'CONGRATS FOR SOLVING ✅' if results['valid_submission'] else 'STILL NEEDS IMPROVEMENT ❌'}")
    if not results['valid_submission']:
        print("\n💡 Tips:")
        print("- Make sure you use auxiliary qubits with proper quantum interference")
        print("- Apply Hadamard gates before and after the controlled operation")
        print("- Always reset qubits after use")
        print("- The algorithm should distinguish between I and -I operations")
    sys.exit(0 if results['valid_submission'] else 1)


if __name__ == "__main__":
    main()
