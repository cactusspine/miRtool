jQuery(document).ready(function() {
	//hide field and when species selected show the 3rd field set
    $('#humanDatabase').hide();
    $('#mouseDatabase').hide();    
    $('#org').change(function(){
    if($('#org option:selected').val() == "human"){
        $('#humanDatabase').show();
        $('#mouseDatabase').hide();
    }else{
    $('#mouseDatabase').show();
    $('#humanDatabase').hide();
    }
    });    
    //End hide field and when species selected show the 3rd field set
    
    //check selectall checkbox and check all the box    
    $('#selectall').click(function(event) {  //on click 
        if(this.checked) { // check select status
            $('.checkboxAll').each(function() { //loop through each checkbox
                this.checked = true;  //select all checkboxes with class "checkbox1"               
            });
        }else{
            $('.checkboxAll').each(function() { //loop through each checkbox
                this.checked = false; //deselect all checkboxes with class "checkbox1"                       
            });         
        }
    });
    //end select all checkbox
    //check recommanded checkbox and check/uncheck all the box
    $('#recommanded').click(function(event) {  //on click 
        if(this.checked) { // check select status
            $('.checkboxAll').each(function() { //loop through each checkbox
                this.checked = false; //deselect all checkboxes with class "checkbox1"                       
            });         
            $('.recommanded').each(function() { //loop through each checkbox
                this.checked = true;  //select all checkboxes with class "checkbox1"               
            });
        }else{
            $('.checkboxAll').each(function() { //loop through each checkbox
                this.checked = false; //deselect all checkboxes with class "checkbox1"                       
            });         
        }
    });
    //end check recommanded checkbox and check/uncheck  all the box
    //check minimum checkbox and check/uncheck all the box
    $('#minimum').click(function(event) {  //on click 
        if(this.checked) { // check select status
            $('.checkboxAll').each(function() { //loop through each checkbox
                this.checked = false; //deselect all checkboxes with class "checkbox1"                       
            });         
            $('.minimum').each(function() { //loop through each checkbox
                this.checked = true;  //select all checkboxes with class "checkbox1"               
            });
        }else{
            $('.checkboxAll').each(function() { //loop through each checkbox
                this.checked = false; //deselect all checkboxes with class "checkbox1"                       
            });         
        }
    });
    //end check minimum checkbox and check/uncheck  all the box
    //fill the Category for id type
    fillCategory(1);  
    //End_fill the Category for id type 

	
	
	});
