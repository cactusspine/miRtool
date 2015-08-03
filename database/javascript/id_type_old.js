function fillCategory(){
//	this function is used to fill the category list on load
	addOption(document.drop_list.Category, "human", "human", "");
	addOption(document.drop_list.Category, "mouse", "mouse", "");
	addOption(document.drop_list.Category, "yeast", "yeast", "");
	SelectSubCat();
}

function SelectSubCat(){
// ON selection of category this function will work
	removeAllOptions(document.drop_list.SubCat);
	var selectbox = document.drop_list.SubCat;
//	alert("selectbox : "+selectbox);
//	addOption(selectbox, "", "SubCat", "");
//	alert("value : "+document.drop_list.Category.value);
	if(document.drop_list.Category.value == 'human'){
		addOption(selectbox, "ensembl_gene_id", "Ensembl Gene ID(s)");
                addOption(selectbox, "ensembl_transcript_id", "Ensembl Transcript ID(s)");
                addOption(selectbox, "ensembl_peptide_id", "Ensembl protein ID(s)");
                addOption(selectbox, "agilent_cgh", "Agilent cgh(s)");
                addOption(selectbox, "agilent_probe", "Agilent Probe(s)");
                addOption(selectbox, "embl", "EMBL ID(s)");
                addOption(selectbox, "entrezgene", "EntrezGene ID(s)");
                addOption(selectbox, "go", "GO ID(s)");
                addOption(selectbox, "hgnc_id", "HGNC ID");
                addOption(selectbox, "hgnc_symbol", "HGNC symbol");
                addOption(selectbox, "illumina_v1", "Illumina v1 ID(s)");
                addOption(selectbox, "illumina_v2", "Illumina v2 ID(s)");
                addOption(selectbox, "ipi", "IPI ID(s)");
                addOption(selectbox, "mim_gene_accession", "MIM Gene Accession(s)");
                addOption(selectbox, "mim_morbid_accession", "MIM Morbid Accession(s)");
                addOption(selectbox, "mirbase", "miRBase ID(s)");
                addOption(selectbox, "pdb", "PDB ID(s)");
                addOption(selectbox, "protein_id", "Protein ID(s)");
                addOption(selectbox, "refseq_dna", "Refseq DNA ID(s)");
                addOption(selectbox, "refseq_peptide", "Refseq protein ID(s)");
                addOption(selectbox, "ucsc", "UCSC ID(s)");
                addOption(selectbox, "uniprot_sptrembl", "UniProt/TrEMBL ID(s)");
                addOption(selectbox, "uniprot_swissprot", "UniProt/Swissprot ID(s)");
                addOption(selectbox, "uniprot_swissprot_accession", "UniProt/Swissprot Accession(s)");
                addOption(selectbox, "unigene", "Unigene ID(s)");
                addOption(selectbox, "uniprot_varsplice_id", "UniProt Varsplice ID(s)");
                addOption(selectbox, "hpa_id", "Human Protein Atlas Antibody ID");
                addOption(selectbox, "affy_hc_g110", "Affy hc g110 ID(s)");
                addOption(selectbox, "affy_hg_focus", "Affy hg focus ID(s)");
                addOption(selectbox, "affy_hg_u95a", "Affy hg u95a ID(s)");
                addOption(selectbox, "affy_hg_u95av2", "Affy hg u95av2 ID(s)");
                addOption(selectbox, "affy_hg_u95b", "Affy hg u95b ID(s)");
                addOption(selectbox, "affy_hg_u95c", "Affy hg u95c ID(s)");
                addOption(selectbox, "affy_hg_u95d", "Affy hg u95d ID(s)");
                addOption(selectbox, "affy_hg_u95e", "Affy hg u95e ID(s)");
                addOption(selectbox, "affy_hg_u133a_2", "Affy hg u133a 2 ID(s)");
                addOption(selectbox, "affy_hg_u133a", "Affy hg u133a ID(s)");
                addOption(selectbox, "affy_hg_u133b", "Affy hg u133b ID(s)");
                addOption(selectbox, "affy_hg_u133_plus_2", "Affy hg u133 plus 2 ID(s)");
                addOption(selectbox, "affy_hugenefl", "Affy hugenefl ID(s)");
                addOption(selectbox, "affy_u133_x3p", "Affy u133 x3p ID(s)");
	}
	if(document.drop_list.Category.value == 'mouse'){
                addOption(selectbox, "ensembl_gene_id", "Ensembl Gene ID(s)");
                addOption(selectbox, "ensembl_transcript_id", "Ensembl Transcript ID(s)");
                addOption(selectbox, "ensembl_peptide_id", "Ensembl protein ID(s)");
                addOption(selectbox, "agilent_probe", "Agilent Probe(s)");
                addOption(selectbox, "embl", "EMBL ID(s)");
                addOption(selectbox, "entrezgene", "EntrezGene ID(s)");
                addOption(selectbox, "go", "GO ID(s)");
                addOption(selectbox, "illumina_v1", "Illumina v1 ID(s)");
                addOption(selectbox, "illumina_v2", "Illumina v2 ID(s)");
                addOption(selectbox, "imgt_gene_db", "IMGT gene db ID(s)");
                addOption(selectbox, "imgt_ligm_db", "IMGT/LIGM-DB ID(s)");
                addOption(selectbox, "ipi", "IPI ID(s)");
                addOption(selectbox, "mgi_id", "MGI ID");
                addOption(selectbox, "mgi_symbol", "MGI symbol");
                addOption(selectbox, "mirbase", "miRBase ID(s)");
                addOption(selectbox, "pdb", "PDB ID(s)");
                addOption(selectbox, "protein_id", "Protein ID(s)");
                addOption(selectbox, "refseq_dna", "Refseq DNA ID(s)");
                addOption(selectbox, "refseq_peptide", "Refseq protein ID(s)");
                addOption(selectbox, "ucsc", "UCSC ID(s)");
                addOption(selectbox, "uniprot_sptrembl", "UniProt/TrEMBL ID(s)");
                addOption(selectbox, "uniprot_swissprot", "UniProt/Swissprot ID(s)");
                addOption(selectbox, "uniprot_swissprot_accession", "UniProt/Swissprot Accession(s)");
                addOption(selectbox, "unigene", "Unigene ID(s)");
                addOption(selectbox, "uniprot_varsplice_id", "UniProt Varsplice ID(s)");
                addOption(selectbox, "affy_mg_u74a", "Affy mg u74a ID(s)");
                addOption(selectbox, "affy_mg_u74av2", "Affy mg u74av2 ID(s)");
                addOption(selectbox, "affy_mg_u74b", "Affy mg u74b ID(s)");
                addOption(selectbox, "affy_mg_u74bv2", "Affy mg u74bv2 ID(s)");
                addOption(selectbox, "affy_mg_u74c", "Affy mg u74c ID(s)");
                addOption(selectbox, "affy_mg_u74cv2", "Affy mg u74cv2 ID(s)");
                addOption(selectbox, "affy_moe430a", "Affy moe430a ID(s)");
                addOption(selectbox, "affy_moe430b", "Affy moe430b ID(s)");
                addOption(selectbox, "affy_mouse430_2", "Affy mouse430 2 ID(s)");
                addOption(selectbox, "affy_mouse430a_2", "Affy mouse430a 2 ID(s)");
                addOption(selectbox, "affy_mu11ksuba", "Affy mu11ksuba ID(s)");
                addOption(selectbox, "affy_mu11ksubb", "Affy mu11ksubb ID(s)");
                addOption(selectbox, "affy_moex_1_0_st_v1", "Affymetrix Microarray moex 1 0 st v1 ID(s)");
                addOption(selectbox, "affy_mogene_1_0_st_v1", "Affymetrix Microarray mogene 1 0 st v1 ID(s)");
	}
	if(document.drop_list.Category.value == 'yeast'){
		addOption(selectbox, "ensembl_gene_id", "Ensembl Gene ID(s)");
                addOption(selectbox, "ensembl_transcript_id", "Ensembl Transcript ID(s)");
                addOption(selectbox, "ensembl_peptide_id", "Ensembl protein ID(s)");
                addOption(selectbox, "embl", "EMBL ID(s)");
                addOption(selectbox, "entrezgene", "EntrezGene ID(s)");
                addOption(selectbox, "go", "GO ID(s)");
                addOption(selectbox, "pdb", "PDB ID(s)");
                addOption(selectbox, "protein_id", "Protein ID(s)");
                addOption(selectbox, "refseq_peptide", "Refseq protein ID(s)");
                addOption(selectbox, "sgd", "Sgd ID(s)");
                addOption(selectbox, "uniprot_sptrembl", "UniProt/TrEMBL ID(s)");
                addOption(selectbox, "uniprot_swissprot", "UniProt/Swissprot ID(s)");
                addOption(selectbox, "uniprot_swissprot_accession", "UniProt/Swissprot Accession(s)");
                addOption(selectbox, "uniprot_varsplice_id", "UniProt Varsplice ID(s)");
                addOption(selectbox, "affy_yeast_2", "Affy yeast 2 ID(s)");
                addOption(selectbox, "affy_yg_s98", "Affy yg s98 ID(s)");
	}
}

function removeAllOptions(selectbox) {
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
	if(value=="human"){
                optn.setAttribute("selected","selected");
		
        }
	if(value=="ensembl_gene_id"){
		optn.setAttribute("selected","selected");
	}
	selectbox.options.add(optn);
}
