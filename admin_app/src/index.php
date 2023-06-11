<?php
// Connect to database
$dbhost = getenv('DB_HOST');
$dbname = getenv('DB_NAME');
$dbuser = getenv('DB_USER');
$dbpass = getenv('DB_PASS');
$db = mysqli_connect($dbhost, $dbuser, $dbpass, $dbname);
$authorized = false;



// Get user input
if (!empty($_GET)) {
    $user = $_GET['username'];
    $pass = $_GET['password'];
    // Validate user
    $query = 'SELECT * FROM users WHERE username="' . $user . '" AND password="' . $pass . '"';
    $result = mysqli_query($db, $query);
    if (!$result) {
        $error = mysqli_error($db);
    } else if (mysqli_num_rows($result) > 0) {
        $authorized = true;
        $rows = mysqli_fetch_assoc($result);
        $user = $rows['username'];
        $pass = $rows['password'];
    } else {
        $query = 'SELECT * FROM users WHERE username="' . $user . '"';
        $result = mysqli_query($db, $query);
        if (!$result || mysqli_num_rows($result) == 0) {
            $error = "Invalid username.";
        } else {
            $error = "Invalid password.";
        }
    }
    // Close database connection
    mysqli_close($db);
}
?>

<!-- Render HTML-->
<!DOCTYPE html>
<html>

<head>
    <style>
        * {
            margin: 0;
            padding: 0;
        }

        body {
            background: gray;
        }

        div {
            width: 75%;
            margin-left: auto;
            margin-right: auto;
            background-color: white;
            padding: 50px;
            box-shadow: 0 2px 15px rgba(0, 0, 0, 0.35);
        }

        form.login {
            display: block;
            width: 400px;
            margin-top: 20%;
            margin-left: auto;
            margin-right: auto;
            padding: 40px;
            background: white;
            color: black;
            border-radius: 10px;
            box-shadow: 0 2px 15px rgba(0, 0, 0, 0.35);
        }

        h2 {
            font-family: Tahoma, sans-serif;
            font-size: 24px;
            margin-bottom: 18px;
        }

        p {
            font-family: Tahoma, sans-serif;
            font-size: 15px;
            margin-bottom: 4px;
        }

        .error {
            margin-top: 12px;
            padding: 4px 6px;
            background-color: red;
            color: white;
            font-weight: bold;
            border-radius: 4px;
        }

        .hint {
            font-size: 14px;
            font-style: italic;
            text-align: center;
            color: white;
            margin: 20px 0;
        }

        label {
            display: inline-block;
            width: 90px;
        }

        input {
            padding: 7px 14px;
            border: none;
            border-radius: 4px;
            box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.35);
        }

        input[type=submit] {
            background-color: blue;
            color: white;
            font-weight: bold;
            box-shadow: none;
            cursor: pointer;
        }

        input.logout {
            position: absolute;
            right: 13%;
            top: 50px;
        }
    </style>
</head>

<body>

    <!-- Login page -->
    <?php if (!$authorized) { ?>
        <form class="login" method="GET">
            <h3>flag_f109947976be6b3eab506d48f648698d<h3>
                    <br>

                    <h2>Please log in:</h2>
                    <p><label>Username:</label><input type="text" name="username" value="<?php if (!empty($user))
                        echo $user; ?>"></p>
                    <p><label>Password:&nbsp;</label><input type="password" name="password" value="">&nbsp;
                        <input type="submit" value="Go">
                    </p>
                    <?php if (!empty($error))
                        echo '<p class="error">' . $error . '</p>'; ?>
        </form>


        <!-- Successful injection page -->
    <?php } else if ($_GET['username'] != $user || $_GET['password'] != $pass) { ?>
            <div>
                <h2>Welcome
                <?php echo $user; ?>!
                </h2>
                <p>Congratulations!</p>
                <p>You have successfully bypassed authentication security.</p>
                <h3>flag_b4494240702252a1964da719bd046033</h3>
                <p>&nbsp;</p>
                <p><img src="images.jpeg" alt="Hacker" style="width: 100%"></p>
                <form><input class="logout" type="submit" value="Logout"></form>
            </div>

            <!-- Normal user home page -->
    <?php } else { ?>
            <div>
                <h2>Welcome
                <?php echo $user; ?>!
                </h2>
                <p>Congratulations on remembering your password.</p>
                <p>You didn't pass the challenge, however. Try again!</p>
                <p>&nbsp;</p>
                <form><input class="logout" type="submit" value="Logout"></form>
            </div>

    <?php } ?>

</body>

</html>