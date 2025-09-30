<?php
function initializeDatabase()
{
  $db_dir = __DIR__ . '/../db';
  $db_file = $db_dir . '/employees.db';

  // Only initialize if database doesn't exist
  if (file_exists($db_file)) {
    return true;
  }

  try {
    if (!is_dir($db_dir)) {
      mkdir($db_dir, 0755, true);
    }

    $pdo = new PDO("sqlite:$db_file");
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Create employees table
    $pdo->exec("CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role_id INTEGER NOT NULL,
            department TEXT NOT NULL
        )");

    // Create employee_reviews table (contains the flag)
    $pdo->exec("CREATE TABLE IF NOT EXISTS employee_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            review_text TEXT NOT NULL,
            rating INTEGER NOT NULL,
            bonus TEXT NOT NULL
        )");

    // Insert employees
    $employees = [
      // Developers (role_id: 3)
      ['EMP001', 'Rajesh Kumar', 'rajesh.kumar@vishalmega.mart', '945-573-9710', 'rajesh_dev', 'VFXHmDyxTWYB4kd2', 3, 'IT'],
      ['EMP002', 'Priya Sharma', 'priya.sharma@vishalmega.mart', '748-476-9320', 'priya_dev', 'rEce9N8LDX9CXxYy', 3, 'IT'],
      ['EMP003', 'Divy Jakhotiya', 'f20240647@goa.bits-pilani.ac.in', '600-513-7134', 'devdivy', 'xEkVB9RhQ3MSHVbh', 3, 'IT'],

      // Customer Support (role_id: 5) - These are fetched by default
      ['EMP004', 'Sunita Gupta', 'sunita.gupta@vishalmega.mart', '762-834-6182', 'sunita_cs', 'qjaynGSGwNFjcTvt', 5, 'Customer Service'],
      ['EMP005', 'Ravi Patel', 'ravi.patel@vishalmega.mart', '477-864-2126', 'ravi_cs', 'rjaGBpAUPdXTnmce', 5, 'Customer Service'],
      ['EMP006', 'Meera Joshi', 'meera.joshi@vishalmega.mart', '411-504-7836', 'meera_cs', 'gp8DpHKNsN6aRDfC', 5, 'Customer Service'],
      ['EMP007', 'Deepak Yadav', 'deepak.yadav@vishalmega.mart', '167-527-5262', 'deepak_cs', 'ZMR9L4LRrEk5Z6m9', 5, 'Customer Service'],
      ['EMP008', 'Kavita Reddy', 'kavita.reddy@vishalmega.mart', '339-110-3513', 'kavita_cs', 'S4Ex8MyYmkN72C2G', 5, 'Customer Service'],

      // Security Guards (role_id: 5)
      ['EMP009', 'Suresh Babu', 'suresh.babu@vishalmega.mart', '708-904-4146', 'suresh_sg', 'Mju7sBPC7Fj39Wt9', 5, 'Security'],
      ['EMP010', 'Ramesh Chandra', 'ramesh.chandra@vishalmega.mart', '512-790-5230', 'ramesh_sg', 't4bL8JD2vsA2TNeK', 5, 'Security'],
      ['EMP011', 'Vikram Singh', 'vikram.singh@vishalmega.mart', '119-308-1605', 'vikram_sg', 'Rsn2aYWuTtVyv8sq', 5, 'Security'],
      ['EMP012', 'Mahesh Kumar', 'mahesh.kumar@vishalmega.mart', '860-424-4721', 'mahesh_sg', 'jbfTpVVuhpRhSrmV', 5, 'Security'],
      ['EMP013', 'Dinesh Sharma', 'dinesh.sharma@vishalmega.mart', '813-663-8448', 'dinesh_sg', 'D4V3gpKP38N32Pa7', 5, 'Security'],

      // Admins (role_id: 2)
      ['EMP014', 'Arjun Malhotra', 'arjun.malhotra@vishalmega.mart', '528-243-7168', 'admin', 'dgdrfb2wyn7BjPvu', 2, 'Administration'],
      ['EMP015', 'Shreya Agarwal', 'shreya.agarwal@vishalmega.mart', '668-670-6216', 'shreya_admin', '5jPnvFe9qp3S65H6', 2, 'Administration'],

      // Managers (role_id: 2)
      ['EMP016', 'Rohit Verma', 'rohit.verma@vishalmega.mart', '903-916-8379', 'rohit_mgr', 'Kcn8feqFnUxCDZdL', 2, 'Management'],
      ['EMP017', 'Neha Kapoor', 'neha.kapoor@vishalmega.mart', '375-853-6288', 'neha_mgr', 'mByzpRDmP3h3rnC2', 2, 'Management'],

      // Chief Security Guard (role_id: 1) - The target!
      ['EMP069', 'Yashwant Singh Thakur', 'headsec@vishalmega.mart', '877-810-0846', 'csg_yashwant', 'aByuBYGV8hrUpVWT', 1, 'Security']
    ];

    $stmt = $pdo->prepare("INSERT INTO employees (employee_id, name, email, phone, username, password, role_id, department) VALUES (?, ?, ?, ?, ?, ?, ?, ?)");

    foreach ($employees as $emp) {
      $stmt->execute($emp);
    }

    // Insert employee reviews (including the flag for CSG)
    $reviews = [
      ['EMP014', 'Outstanding administrative skills.', 9, '10000'],
      ['EMP001', 'Excellent coding skills.', 8, '20500'],
      ['EMP004', 'Great customer service.', 8, '14000'],
      ['EMP009', 'Reliable security guard.', 7, '12600'],
      ['EMP002', 'Consistently delivers high-quality code.', 8, '18750'],
      ['EMP016', 'Strong leadership qualities and strategic thinking.', 9, '25000'],
      ['EMP069', 'Exceptional security leadership. But won\'t get a big bonus :)', 10, 'InductionCTF{p4yd4y_p4yd4y_1n7171473_b0nu5_upgr4d3_pr070c0l}'],
      ['EMP005', 'Exceptional customer satisfaction scores.', 7, '13500'],
      ['EMP010', 'Diligent security guard with excellent patrol records.', 6, '11800'],
      ['EMP015', 'Efficient administrative support and excellent organizational skills.', 7, '15200'],
    ];

    $stmt = $pdo->prepare("INSERT INTO employee_reviews (employee_id, review_text, rating, bonus) VALUES (?, ?, ?, ?)");

    foreach ($reviews as $review) {
      $stmt->execute($review);
    }

    return true;

  } catch (Exception $e) {
    error_log("Database initialization failed: " . $e->getMessage());
    return false;
  }
}

function getDatabaseConnection()
{
  $db_file = __DIR__ . '/../db/employees.db';

  // Initialize database if it doesn't exist
  if (!file_exists($db_file)) {
    if (!initializeDatabase()) {
      throw new Exception('Failed to initialize database');
    }
  }

  $pdo = new PDO("sqlite:$db_file");
  $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

  return $pdo;
}
?>