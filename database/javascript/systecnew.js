jQuery(function() {

   //check all script -----------------------------------
    $('#selectall').click(function(event) {  //on click 
        if(this.checked) { // check select status
            $('.checkbox1').each(function() { //loop through each checkbox
                this.checked = true;  //select all checkboxes with class "checkbox1"               
            });
        }else{
            $('.checkbox1').each(function() { //loop through each checkbox
                this.checked = false; //deselect all checkboxes with class "checkbox1"                       
            });         
        }
    });
    //uncheck/check all script-----------------------------
    
    //------expand all /collapse all------------------------
    $('#expand').click(function(event) {  //on click         
            $('.mycheckbox').each(function() { //loop through each checkbox
                this.checked = true;  //select all checkboxes with class "          
            });            
        
    });
       $('#collapse').click(function(event) {  //on click         
            $('.mycheckbox').each(function() { //loop through each checkbox

                this.checked = false;  //select all checkboxes with class            
            });            
        
    });
   $('.drop-wrap').on('click',function(){
      $('.drop-wrap ul').slideToggle();
   });
  //----end--expand all /collapse all------------------------
 //--------get info from check box and open biocompendium-----------
    $("#biocompendium_L").click(function(){
var selectedLanguage = new Array();
$('input[name="chb"]:checked').each(function() {
selectedLanguage.push(this.value);
});
var selectedLanguageS = selectedLanguage.join("__");

   // http://biocompendium.embl.de/cgi-bin/biocompendium.cgi?section=upload_gene_lists_tamahud&background=whole_genome&org=human&gene_list1=human%0Agene_list_1%0Ahgnc_symbol%0APDGFRA__KIT__TP53__KIT
window.open ("http://biocompendium.embl.de/cgi-bin/biocompendium.cgi?section=upload_gene_lists_tamahud&background=whole_genome&org=human&gene_list1=human%0Agene_list_1%0Arefseq%0A"+selectedLanguageS, "mywindow","status=1,toolbar=1");
});
 //-End---------get info from check box and open biocompendium----------
     //--------get info from check box and open KEGG DAVID -----------
$("#kegg_L").click(function(){
var selectedid = new Array();
$('input[name="chb"]:checked').each(function() {
selectedid.push(this.value);
});
var selectedidS = selectedid.join(",");
window.open ("http://david.abcc.ncifcrf.gov/api.jsp?type=REFSEQ_MRNA&ids="+selectedidS+"&tool=chartReport&annot=KEGG_PATHWAY", "mywindow1","status=1,toolbar=1");
});
 //-End---------get info from check box and open KEGG DAVID---------
 //--------get info from check box and open GO enrichment-----------
$("#go_L").click(function(){
var selectedid = new Array();
$('input[name="chb"]:checked').each(function() {
selectedid.push(this.value);
});
var selectedidS = selectedid.join(",");
window.open ("http://david.abcc.ncifcrf.gov/api.jsp?type=REFSEQ_MRNA&ids="+selectedidS+" &tool=chartReport&annot=GOTERM_BP_FAT,GOTERM_CC_FAT,GOTERM_MF_FAT", "mywindow2","status=1,toolbar=1");
});
 //-End---------get info from check box and open GO Enrichment---------

});
