<?php
require_once 'includes/session.php';
require_once 'includes/db_init.php';

if (!isLoggedIn()) {
  header('Location: index.php');
  exit;
}

if (!isAdmin()) {
  die('Access Denied: Admin privileges required. Come back as an admin.');
}

$reviews = [];
$employee_query = '';
$error = '';

try {
  $pdo = getDatabaseConnection();
  $sql = "SELECT e.employee_id, e.name, e.department, r.review_text, r.rating 
            FROM employees e 
            JOIN employee_reviews r ON e.employee_id = r.employee_id";

  if (isset($_GET['employee_reviews']) && !empty($_GET['employee_reviews'])) {
    $employee_query = $_GET['employee_reviews'];
    // VULNERABLE: Direct string concatenation for SQLMap exploitation
    $sql = "SELECT e.employee_id, e.name, e.department, r.review_text, r.rating 
                FROM employees e 
                JOIN employee_reviews r ON e.employee_id = r.employee_id 
                WHERE e.name LIKE '%{$employee_query}%'";
  }

  $result = $pdo->query($sql);
  $reviews = $result->fetchAll(PDO::FETCH_ASSOC);

} catch (Exception $e) {
  $error = 'Database error: ' . $e->getMessage();
}

$current_user = getAuthFromCookie();
?>

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VMM Employee Reviews - Admin Panel</title>
  <style>
    /* Same CSS as before */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    :root {
      --vmm-red: #d9232d;
      --vmm-blue: #004a99;
      --vmm-gold: #ffd700;
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: 'Poppins', sans-serif;
      background: #f5f5f5;
      min-height: 100vh;
    }

    .navbar {
      background: var(--vmm-red);
      color: white;
      padding: 15px 0;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .nav-container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .nav-brand {
      font-size: 1.8em;
      font-weight: 700;
    }

    .nav-links {
      display: flex;
      gap: 20px;
      align-items: center;
    }

    .nav-links a {
      color: white;
      text-decoration: none;
      padding: 8px 16px;
      border-radius: 5px;
      transition: background 0.3s;
    }

    .nav-links a:hover {
      background: rgba(255, 255, 255, 0.2);
    }

    .container {
      max-width: 1200px;
      margin: 40px auto;
      padding: 0 20px;
    }

    .admin-header {
      background: linear-gradient(135deg, var(--vmm-gold), #ffed4e);
      color: #856404;
      padding: 20px;
      border-radius: 10px;
      margin-bottom: 30px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .search-section {
      background: white;
      padding: 25px;
      border-radius: 10px;
      margin-bottom: 30px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .search-form {
      display: flex;
      gap: 15px;
      align-items: end;
    }

    .form-group {
      flex: 1;
    }

    .form-group label {
      display: block;
      margin-bottom: 8px;
      color: var(--vmm-blue);
      font-weight: 600;
    }

    .form-group input {
      width: 100%;
      padding: 12px 15px;
      border: 2px solid #e1e1e1;
      border-radius: 8px;
      font-size: 1em;
    }

    .search-btn {
      background: var(--vmm-blue);
      color: white;
      border: none;
      padding: 12px 25px;
      border-radius: 8px;
      font-weight: 600;
      cursor: pointer;
      height: fit-content;
    }

    .review-card {
      background: white;
      padding: 25px;
      border-radius: 10px;
      margin-bottom: 20px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .employee-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 15px;
      padding-bottom: 15px;
      border-bottom: 2px solid #e1e1e1;
    }

    .employee-name {
      color: var(--vmm-red);
      font-size: 1.4em;
      font-weight: 600;
    }

    .employee-dept {
      color: var(--vmm-blue);
      font-weight: 500;
    }

    .rating {
      background: var(--vmm-gold);
      color: #856404;
      padding: 8px 15px;
      border-radius: 20px;
      font-weight: bold;
    }

    .review-text {
      color: #333;
      line-height: 1.6;
      margin-top: 15px;
    }

    .employee-id {
      background: var(--vmm-blue);
      color: white;
      padding: 4px 12px;
      border-radius: 15px;
      font-size: 0.9em;
      display: inline-block;
      margin-top: 10px;
    }

    .error {
      background: #f8d7da;
      color: #721c24;
      padding: 15px;
      border-radius: 8px;
      margin-bottom: 20px;
      border: 1px solid #f5c6cb;
    }
  </style>
</head>

<body>
  <nav class="navbar">
    <div class="nav-container">
      <div class="nav-brand">VMM EMS</div>
      <div class="nav-links">
        <a href="search.php">Directory</a>
        <a href="review.php">Reviews</a>
        <span>Welcome, <?php echo htmlspecialchars($current_user['name']); ?></span>
        <a href="logout.php">Logout</a>
      </div>
    </div>
  </nav>

  <div class="container">
    <div class="admin-header">
      <h2>🔐 Employee Reviews - Admin Access</h2>
      <p>View comprehensive employee performance reviews and ratings.</p>
      <p>Admin note: Review if management has given correct bonuses.</p>
    </div>

    <div class="search-section">
      <form class="search-form" method="GET">
        <div class="form-group">
          <label for="employee">Search Employee Reviews</label>
          <input type="text" id="employee" name="employee_reviews" value="<?php echo htmlspecialchars($employee_query); ?>"
            placeholder="Enter employee name...">
        </div>
        <button type="submit" class="search-btn">Search Reviews</button>
      </form>
    </div>

    <?php if ($error): ?>
      <div class="error"><?php echo htmlspecialchars($error); ?></div>
    <?php endif; ?>

    <?php foreach ($reviews as $review): ?>
      <div class="review-card">
        <div class="employee-header">
          <div>
            <div class="employee-name"><?php echo htmlspecialchars($review['name']); ?></div>
            <div class="employee-dept"><?php echo htmlspecialchars($review['department']); ?> Department</div>
            <div class="employee-id"><?php echo htmlspecialchars($review['employee_id']); ?></div>
          </div>
          <div class="rating">⭐ <?php echo $review['rating']; ?>/10</div>
        </div>
        <div class="review-text"><?php echo htmlspecialchars($review['review_text']); ?></div>
      </div>
    <?php endforeach; ?>

    <?php if (empty($reviews) && !$error): ?>
      <div style="text-align: center; padding: 40px; color: #666;">
        <h3>No reviews found</h3>
        <p>Try adjusting your search criteria.</p>
      </div>
    <?php endif; ?>
  </div>
</body>

</html>