<?php
 
session_start();
 
if(isset($_GET['logout'])){    
     
    //Simple exit message
    $logout_message = "<div class='msgln'><span class='left-info'>User <b class='user-name-left'>". $_SESSION['name'] ."</b> has left the chat session.</span><br></div>";
    file_put_contents("log.html", $logout_message, FILE_APPEND | LOCK_EX);
     
    session_destroy();
    header("Location: index.php"); //Redirect the user
}
 
if(isset($_POST['enter'])){
    if($_POST['name'] != ""){
        $_SESSION['name'] = stripslashes(htmlspecialchars($_POST['name']));
    }
    else{
        echo '<span class="error">Please type in a name</span>';
    }
}
 
function loginForm(){
    echo
    '<div id="loginform">
    <p>Please enter your name to continue!</p>
    <form action="index.php" method="post">
      <label for="name">User Name:</label>
      <input type="text" name="name" id="name" />
      <input type="submit" name="enter" id="enter" value="Enter" />
    </form>
  </div>';
}
 
?>
 
<!DOCTYPE html>
<html lang="en">
    <head>

 <title>AskME.AI</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!--<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css"> -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lato">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat"> 
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

<link href="style.css" rel="stylesheet">
<style>
    body,
    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        font-family: "Lato", sans-serif
    }

    .w3-bar,
    h1,
    button {
        font-family: "Montserrat", sans-serif
    }

    .fa-anchor,
    .fa-coffee {
        font-size: 200px
    }
</style>
        <link rel="stylesheet" href="style.css" />
    </head>
    <body>
	
	   <header style="padding:128px 16px"  >
        <div class="img-back"></div>
        <h1 class="askme">AskMe.AI</h1>
		<br><br>
        <p class="treehacks">TreeHacks 2021</p>
		<form name="process" action="">           
               <input class="button" name="processQ" type="submit" id="processQ" value="Process" />
        </form>
        
      </header>
    
      <br>
      <br>
    <?php
    if(!isset($_SESSION['name'])){
        loginForm();
    }
    else {
    ?>
    <div class="row no-gutters">
        <div class="col-md-6 no-gutters">
            <!-- Left side -->
            <div class="leftside">        
				<div id="wrapper">
					<div id="menu">
					<p class="welcome">Welcome, <b><?php echo $_SESSION['name']; ?></b></p>
					<p class="logout"><a id="exit" href="#">Exit Chat</a></p>
				</div>
 
            <div id="chatbox">
            <?php
            if(file_exists("log.html") && filesize("log.html") > 0){
                $contents = file_get_contents("log.html");          
                echo $contents;
            }
            ?>
            </div>
 
            <form name="message" action="">
                <input name="usermsg" type="text" id="usermsg" />
                <input name="submitmsg" type="submit" id="submitmsg" value="Send" />
            </form>
        </div>
		</div>
		 </div>
		   <div class="col-md-6 no-gutters">
            <!-- Left side -->
            <div class="rightside">        
				<div id="wrapper">
					<div id="menu">
					<p class="welcome">Response:</b></p>
					 
				</div>
 
            <div id="chatbox1">
            <?php
            if(file_exists("response.html") && filesize("response.html") > 0){
                $contents = file_get_contents("response.html");          
                echo $contents;
            }
            ?>
            </div>
 

        </div>
		</div>
		 </div>
		</div>
		 
          <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script type="text/javascript">
            // jQuery Document
            $(document).ready(function () {
                $("#submitmsg").click(function () {
                    var clientmsg = $("#usermsg").val();
                    $.post("post.php", { text: clientmsg });
                    $("#usermsg").val("");
                    return false;
                });
 
                function loadLog() {
                    var oldscrollHeight = $("#chatbox")[0].scrollHeight - 20; //Scroll height before the request
 
                    $.ajax({
                        url: "log.html",
                        cache: false,
                        success: function (html) {
                            $("#chatbox").html(html); //Insert chat log into the #chatbox div
 
                            //Auto-scroll           
                            var newscrollHeight = $("#chatbox")[0].scrollHeight - 20; //Scroll height after the request
                            if(newscrollHeight > oldscrollHeight){
                                $("#chatbox").animate({ scrollTop: newscrollHeight }, 'normal'); //Autoscroll to bottom of div
                            }   
                        }
                    });
                }
 
               function loadResponseLog() {
                    var oldscrollHeight = $("#chatbox1")[0].scrollHeight - 20; //Scroll height before the request
 
                    $.ajax({
                        url: "response.html",
                        cache: false,
                        success: function (html) {
                            $("#chatbox1").html(html); //Insert chat log into the #chatbox div
 
                            //Auto-scroll           
                            var newscrollHeight = $("#chatbox1")[0].scrollHeight - 20; //Scroll height after the request
                            if(newscrollHeight > oldscrollHeight){
                                $("#chatbox1").animate({ scrollTop: newscrollHeight }, 'normal'); //Autoscroll to bottom of div
                            }   
                        }
                    });
                }
				
                setInterval (loadLog, 2500);
				setInterval (loadResponseLog, 2500);
 
                $("#exit").click(function () {
                    var exit = confirm("Are you sure you want to end the session?");
                    if (exit == true) {
                    window.location = "index.php?logout=true";
                    }
                });
            });
        </script>
    </body>
</html>
<?php
}
?>
