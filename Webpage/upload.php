<?php
ob_start();
echo "Hey!";
$target_dir = "../../toicalendar/Files/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$name=$_FILES["fileToUpload"]["name"];
echo $_FILES["fileToUpload"]["name"];
echo $_POST["periods"];
//$target_file = $target_dir.$_FILES(["fileToUpload"]["name"]);
$target_file = $target_dir.$_FILES["fileToUpload"]["name"];
echo $target_file;
$uploadOk = 1;
echo $_FILES["fileToUpload"]["size"];
echo $target_file;
$FileType = pathinfo($target_file,PATHINFO_EXTENSION);
// Check file size
if ($_FILES["fileToUpload"]["size"] > 50000) {
    echo "Sorry, your file is too large.";
    $uploadOk = 0;
}
echo $_FILES["fileToUpload"]["size"];
//allow only docx
if($FileType!="docx")
{
	echo "File type is not docx";
	$uploadOk=0;
}
echo $FileType;

// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
    echo "Sorry, your file was not uploaded.";
// if everything is ok, try to upload file
} else {
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
        echo "The file ". basename( $_FILES["fileToUpload"]["name"]). " has been uploaded.";
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
}
echo "Hey!";
echo $name;
exec("/usr/bin/python ../../toicalendar/bin/core_transformation_php.py ".$name.' '.$_POST["periods"]);
exec("zip ../../toicalendar/Files/".$name."_icalendar.zip ../../toicalendar/Files/*.ics");
exec("rm -f ../../toicalendar/Files/*.ics");
//exec("rm -f ../../toicalendar/Files/*.zip"); this line was here, but it did not delete all the zip files and therefore prevent
//the downloads from happening. Not sure why.
if(file_exists("../../toicalendar/Files/".$name."_icalendar.zip"))
{
    echo "file_exists";
    ob_end_clean();
    header('Content-Description: File Transfer');
    header('Content-Type: application/octet-stream');
    header('Content-Disposition: attachment; filename="'.basename("../../toicalendar/Files/".$name."_icalendar.zip").'"');
    header('Expires: 0');
    header('Cache-Control: must-revalidate');
    header('Pragma: public');
    header('Content-Length: ' . filesize("../../toicalendar/Files/".$name."_icalendar.zip"));
    readfile("../../toicalendar/Files/".$name."_icalendar.zip");
}
exec("rm -f ../../toicalendar/Files/*.zip");
?>
