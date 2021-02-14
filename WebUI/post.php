<?php
session_start();
if(isset($_SESSION['name'])){
    $text = $_POST['text'];
     
    $text_message = "<div class='msgln'><span class='chat-time'>".date("g:i A")."</span> <b class='user-name'>".$_SESSION['name']."</b> ".stripslashes(htmlspecialchars($text))."<br></div>";
    file_put_contents("log.html", $text_message, FILE_APPEND | LOCK_EX);
	file_put_contents("question.txt", stripslashes(htmlspecialchars($text))."\n", FILE_APPEND | LOCK_EX);
	//TODO Integrate the API pass the question and get the anser. write the answer into below file
	//example
	/*
	$service_url = 'https://example.com/api/conversations/[CONV_CODE]/messages&apikey=[API_KEY]';
	$curl = curl_init($service_url);
	curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
	$curl_response = curl_exec($curl);
	if ($curl_response === false) {
		$info = curl_getinfo($curl);
		curl_close($curl);
		die('error occured during curl exec. Additioanl info: ' . var_export($info));
	}
	curl_close($curl);
	$decodedResp = json_decode($curl_response);
	if (isset($decodedResp->response->status) && $decodedResp->response->status == 'ERROR') {
		die('error occured: ' . $decodedResp->response->errormessage);
	}
	$answer=$decoded->response;
	*/
	//TODO Uncomment below line for immediate answer for the question
	/*$answer="Im fine";//TODO replace this with the response from API response

	$question="<div class='msgln'><b class='user-name'>Q:</b>".stripslashes(htmlspecialchars($text))."<br>";
	
	$question=$question."<b class='user-name-left'>A:</b>".$answer."<br></div>";
	file_put_contents("response.html",$question,FILE_APPEND | LOCK_EX); */
}
?>
