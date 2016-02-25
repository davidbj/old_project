 function	showHide(panelID)
   {
	  var panel	= document.getElementById(panelID);
	   
		 if	(panel.style.display == "block")
		 {
			panel.style.display	= "none"; 
		 } else	{
			panel.style.display	= "block"; 			 
		 } 
   }  
function forword(url){ 
	 window.location.href = url; 
	} 
 function submitform(action){
	var form=document.getElementById("findform");
	form.action=action;
 	form.submit();  
} 
