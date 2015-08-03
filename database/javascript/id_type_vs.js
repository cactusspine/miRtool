function fillCategory(upload_number){
//	this function is used to fill the category list on load
	var select_category_id = "Category"+upload_number;
//	alert("select_category_id : "+select_category_id);
	var category_selectbox = document.getElementById(select_category_id);
//	alert("category_selectbox : "+category_selectbox);
/*
	addOption(document.drop_list.Category, "human", "human", "");
	addOption(document.drop_list.Category, "mouse", "mouse", "");
	addOption(document.drop_list.Category, "yeast", "yeast", "");
*/
	addOption(category_selectbox, "", "---------------------ncRNAs---------------------", "");
	addOption(category_selectbox, "pseudogene_id", "Pseudogene ID", "");
	addOption(category_selectbox, "mirbase_name", "miRNA Name", "");
	addOption(category_selectbox, "mirbase_id", "miRBase ID", "");
	addOption(category_selectbox, "long_ncrna_id", "Long ncRNA ID", "");
	addOption(category_selectbox, "antisense_rna_id", "Antisense RNA ID", "");
	addOption(category_selectbox, "sirna_id", "siRNA ID", "");
	addOption(category_selectbox, "snorna_id", "snoRNA ID", "");
	addOption(category_selectbox, "snrna_id", "snRNA ID", "");
	addOption(category_selectbox, "trna_id", "tRNA ID", "");
	addOption(category_selectbox, "rrna_id", "rRNA ID", "");
	addOption(category_selectbox, "pirna_id", "piRNA ID", "");
	addOption(category_selectbox, "", "------------Genes/proteins/transcripts------------", "");
	addOption(category_selectbox, "ensembl_gene_id", "Ensembl Gene ID", "");
	addOption(category_selectbox, "ensembl_transcript_id", "Ensembl Transcript ID", "");
	addOption(category_selectbox, "ensembl_peptide_id", "Ensembl protein ID", "");
	addOption(category_selectbox, "embl", "EMBL ID", "");
	addOption(category_selectbox, "entrezgene", "EntrezGene ID", "");
	addOption(category_selectbox, "hgnc_id", "HGNC ID", "");
	addOption(category_selectbox, "hgnc_symbol", "HGNC symbol", "");
	addOption(category_selectbox, "refseq_dna", "Refseq DNA ID", "");
	addOption(category_selectbox, "refseq_peptide", "Refseq protein ID", "");
	addOption(category_selectbox, "ucsc", "UCSC ID", "");
	addOption(category_selectbox, "uniprot_sptrembl", "UniProt/TrEMBL ID", "");
	addOption(category_selectbox, "uniprot_swissprot", "UniProt/Swissprot ID", "");
	addOption(category_selectbox, "uniprot_swissprot_accession", "UniProt/Swissprot Accession", "");

	SelectSubCat(upload_number);
}
function SelectSubCatAll(select_cat_id_full) {
	var reg = new RegExp("Category");
	if (reg.test(select_cat_id_full)) {
//		alert("select_cat_id_full : "+select_cat_id_full);
		select_cat_id = select_cat_id_full.replace("Category", "");
//		alert("from all select_cat_id : "+select_cat_id);
		SelectSubCat(select_cat_id);
	}

}
function SelectSubCat(upload_number){
// ON selection of category this function will work
	var select_sub_cat_id = "SubCat"+upload_number;
//	alert("1.select_sub_cat_id : "+select_sub_cat_id);
	var selectbox = document.getElementById(select_sub_cat_id);
//	alert("selectbox : "+selectbox);
	removeAllOptions(selectbox);
//	addOption(selectbox, "", "SubCat", "");
//	alert("value : "+document.drop_list.Category.value);

	var select_category_id = "Category"+upload_number;
//	alert("select_category_id : "+select_category_id);
	var category_selectbox_value = document.getElementById(select_category_id).value;
//	alert("value : "+category_selectbox_value);	

	if(category_selectbox_value == 'pseudogene_id'){
		addOption(selectbox, "pseudogene_targets", "Pseudogene Parental Genes");
/*
                addOption(selectbox, "ensembl_transcript_id", "Ensembl Transcript ID");
                addOption(selectbox, "ensembl_peptide_id", "Ensembl protein ID");
                addOption(selectbox, "agilent_cgh", "Agilent cgh");
                addOption(selectbox, "agilent_probe", "Agilent Probe");
                addOption(selectbox, "embl", "EMBL ID");
                addOption(selectbox, "entrezgene", "EntrezGene ID");
                addOption(selectbox, "go", "GO ID");
                addOption(selectbox, "hgnc_id", "HGNC ID");
                addOption(selectbox, "hgnc_symbol", "HGNC symbol");
                addOption(selectbox, "illumina_v1", "Illumina v1 ID");
                addOption(selectbox, "illumina_v2", "Illumina v2 ID");
                addOption(selectbox, "ipi", "IPI ID");
                addOption(selectbox, "mim_gene_accession", "MIM Gene Accession");
                addOption(selectbox, "mim_morbid_accession", "MIM Morbid Accession");
                addOption(selectbox, "mirbase", "miRBase ID");
                addOption(selectbox, "pdb", "PDB ID");
                addOption(selectbox, "protein_id", "Protein ID");
                addOption(selectbox, "refseq_dna", "Refseq DNA ID");
		addOption(selectbox, "ascii", "ascii");
*/
	}
	if((category_selectbox_value == 'mirbase_name')||(category_selectbox_value == 'mirbase_id')) {
                addOption(selectbox, "mirna_targets", "miRNA Targets");
	}
	if(category_selectbox_value == 'long_ncrna_id'){
		addOption(selectbox, "long_ncrna_targets", "Long ncRNA Targets");
	}
	if(category_selectbox_value == 'antisense_rna_id'){
		addOption(selectbox, "antisense_rna_targets", "Antisense RNA Targets");
	}
	if(category_selectbox_value == 'sirna_id'){
		addOption(selectbox, "sirna_targets", "siRNA Targets");
	}
	if(category_selectbox_value == 'snorna_id'){
		addOption(selectbox, "snorna_targets", "snoRNA Targets");
	}
	if(category_selectbox_value == 'trna_id'){
		addOption(selectbox, "trna_targets", "tRNA Targets");
	}
	if(category_selectbox_value == 'rrna_id'){
		addOption(selectbox, "rrna_targets", "rRNA Targets");
	}
	if(category_selectbox_value == 'pirna_id'){
		addOption(selectbox, "pirna_targets", "piRNA Targets");
	}
	if((category_selectbox_value == 'ensembl_gene_id')||
	   (category_selectbox_value == 'ensembl_transcript_id')||
           (category_selectbox_value == 'ensembl_peptide_id')||
           (category_selectbox_value == 'embl')||
           (category_selectbox_value == 'entrezgene')||
           (category_selectbox_value == 'hgnc_id')||
	   (category_selectbox_value == 'hgnc_symbol')||
	   (category_selectbox_value == 'refseq_dna')||
	   (category_selectbox_value == 'refseq_peptide')||
	   (category_selectbox_value == 'ucsc')||
	   (category_selectbox_value == 'uniprot_sptrembl')||
	   (category_selectbox_value == 'uniprot_swissprot')||
	   (category_selectbox_value == 'uniprot_swissprot_accession')
          ) {
		addOption(selectbox, "all_ncrna", "All ncRNAs");
		addOption(selectbox, "pseudogene_id", "Pseudogenes (all)");
		addOption(selectbox, "pseudogene_id", "Pseudogenes (processed)");
		addOption(selectbox, "pseudogene_id", "Pseudogenes (duplicated)");
		addOption(selectbox, "mirbase_name", "miRNAs");
		addOption(selectbox, "long_ncrna_id", "Long ncRNAs");
		addOption(selectbox, "antisense_rna_id", "Antisense RNAs");
		addOption(selectbox, "sirna_id", "siRNAs");
		addOption(selectbox, "snorna_id", "snoRNAs", "");
		addOption(selectbox, "snrna_id", "snRNAs");
		addOption(selectbox, "trna_id", "tRNAs");
		addOption(selectbox, "rrna_id", "rRNAs");
		addOption(selectbox, "pirna_id", "piRNAs");
	}

}

function removeAllOptions(selectbox) {
//	alert("2.hello i am removing!!!"+selectbox);
//	alert("from removeAllOptions : "+selectbox);
	var i;
		for(i=selectbox.options.length-1;i>=0;i--) {
			//selectbox.options.remove(i);
                	selectbox.remove(i);
		}
}	

function addOption(selectbox, value, text ){
//	alert("from addOption : "+selectbox);
	var optn = document.createElement("OPTION");
	optn.text = text;
	optn.value = value;
	if(value=="mirbase_name"){
                optn.setAttribute("selected","selected");
		
        }
	if(value=="mirna_targets"){
		optn.setAttribute("selected","selected");
	}
	selectbox.options.add(optn);
}
