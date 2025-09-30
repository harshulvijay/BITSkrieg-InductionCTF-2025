operation DistinguishUOneUMinusOne(u : Qubit => Unit is Adj + Ctl, psi : Qubit) : Int {
    use aux = Qubit();
    H(aux);
    Controlled u([aux], psi);
    H(aux);
    let result = M(aux);
    Reset(aux);
    return result == Zero ? 0 | 1;
}