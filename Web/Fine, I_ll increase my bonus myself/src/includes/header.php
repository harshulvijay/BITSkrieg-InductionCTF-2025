<nav class="navbar">
  <div class="nav-container">
    <div class="nav-brand">VMM EMS</div>
    <div class="nav-links">
      <a href="search.php">Directory</a>
      <a href="review.php">Reviews</a>
      <span>Welcome, <?php echo htmlspecialchars($_SESSION['user']['name']); ?></span>
      <a href="logout.php">Logout</a>
    </div>
  </div>
</nav>