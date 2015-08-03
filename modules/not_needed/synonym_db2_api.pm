package synonym_db2_api;
 
sub get_annotations {
	my $gene_name = shift;
###calling process_genelist routine
	my $process_genelist_result = &process_genelist($gene_name);
	my %process_genelist_result = %$process_genelist_result;
	my $description = $process_genelist_result{$gene_name}{"description"};
	my $id = $process_genelist_result{$gene_name}{"id"};
#print STDERR "ID : $id\n";
#print STDERR "description : $description\n";
###calling annotation_view routine
	my $annotation = &annotation_view($id, $description);
	return $annotation;
} # sub get_annotations { 

sub process_genelist {
	my $gene_list = shift;
	my $org = "human";
	my %result_hash = 
	my @gene_list = ();
	my $text = "";
	my $file_name = "";
	if ($gene_list) {
		@gene_list = split("\n", $gene_list);
	}
	chomp(@gene_list);
	my @tmp = ();
	foreach my $g (@gene_list) {
		$g=~s/\s//g;
		push @tmp, $g;
	}
	@gene_list=&nonRedundantList(\@tmp);
use IO::Socket::INET;
use SocketConf_Synonym_db2;

	my %socket_conf = &SocketConf_Synonym_db2::getSocketConf();

        my $gene_list_str = join("\n",@gene_list);
use hgnc_info;
	my $hgnc_info_result = &hgnc_info::process_genelist($gene_list_str);
	my %hgnc_info_result = %$hgnc_info_result;
	my $method = "get_uniprot_acc";
#print "gene_list_str : $gene_list_str";
        my $msg = $org."\n". $method . "\n" .$gene_list_str.$socket_conf{END_OF_MESSAGE_TAG}."\n";
#print "msg : $msg<br>";

        my $clint_socket = IO::Socket::INET->new( Proto => "tcp",
                                           PeerAddr => $socket_conf{HOST},
                                           PeerPort => $socket_conf{PORT}
                                         );
        my $response = "";
        if ($gene_list_str) {
                $response = $clint_socket->send($msg);
        }
        $/ = "_END_OF_MESSAGE_";
        $response = <$clint_socket>;
        chomp($response);
        $/ = "\n";
#print "response : $response<br>";
        close($clint_socket);
	
	my @entries = split("______", $response); 

  foreach my $e (@entries) {
		my ($name, $pac_str) = split("____", $e);
		my ($uniprot_acc, $description, $database) = split("__", $pac_str);
#print "pac_str : $pac_str\n<br>";
		my $flag="no";
		my $hgnc_id = "";
		my $uniprot_acc_via_hgnc = "";
		my @hgnc2uniprot = @{$hgnc_info_result{$name}};	
		foreach my $hgnc2uniprot (@hgnc2uniprot) {
			($hgnc_id, $uniprot_acc_via_hgnc) = split("_", $hgnc2uniprot);
			if ($uniprot_acc eq $uniprot_acc_via_hgnc) {
								$flag="yes";
							}
						}
						if ($flag eq "no") {
							if ($uniprot_acc_via_hgnc){
								$uniprot_acc = $uniprot_acc_via_hgnc;
use uniprot_info;
								my $new_info = &uniprot_info::process_genelist($uniprot_acc, $org);
								my %new_info = %$new_info;
								$pac_str = $new_info{$uniprot_acc};
								($uniprot_acc, $description, $database) = split("__", $pac_str); 
		 					}		
						}
						$database = uc($database);
						my $id=$database . "|" . $uniprot_acc . "|" . $hgnc_id;
						$result_hash{$name}{"description"} = $description;
						$result_hash{$name}{"id"} = $id;
					}
	return \%result_hash;
} # sub process_genelists {

sub annotation_view {
	my ($uniprot2hgnc, $description) = @_;
	my $org = "human";
	my ($database, $uniprot_pac, $hgnc_id) = split('\|', $uniprot2hgnc);
	$database=lc($database);
#print "database : $database, uniprot_pac : $uniprot_pac, hgnc_id : $hgnc_id\n<br>";
use hgnc_info;
use uniprot_info;
	my $hgnc_annotation = &hgnc_info::get_hgnc_annotation($hgnc_id);
	my %hgnc_annotation = %$hgnc_annotation;
	my $uniprot_annotation = &uniprot_info::get_uniprot_annotation($uniprot_pac, $org, $database);
	my %uniprot_annotation = %$uniprot_annotation;

	my $result_str = "";
#HGNC_ID
	$result_str .= "HGNC_ID: $hgnc_id\n";
	$result_str .= "Symbol: $hgnc_annotation{Approved_Symbol}\n";
	$result_str .= "Name: $hgnc_annotation{Approved_Name}\n";
	$result_str .= "Description: $description\n";
my $previous_symbols = $hgnc_annotation{Previous_Symbols};
$previous_symbols =~ s/__/, /g; 
	$result_str .= "Previous Symbols: $previous_symbols\n";
my $hgnc_synonyms = $hgnc_annotation{Synonym};
my @hgnc_synonyms = split("__",$hgnc_synonyms) if $hgnc_synonyms;
my $uniprot_synonyms = $uniprot_annotation{Synonym}; 
my @uniprot_synonyms = split("__",$uniprot_synonyms) if $uniprot_synonyms;
my @all_synonyms = (@uniprot_synonyms, @uniprot_synonyms);
@all_synonyms = &nonRedundantList(\@all_synonyms);
my $all_synonyms_str=join(", ",@all_synonyms);
	$result_str .= "Synonyms: $all_synonyms_str\n";
#Chromosome
	$result_str .= "Chromosome: $hgnc_annotation{Chromosome}\n";
my $hgnc_refseq = $hgnc_annotation{RefSeq};
my @hgnc_refseq = split("__",$hgnc_refseq) if $hgnc_refseq;
my $uniprot_refseq = $uniprot_annotation{RefSeq}; 
my @uniprot_refseq = split("__",$uniprot_refseq) if $uniprot_refseq;
my @all_refseq = (@uniprot_refseq, @uniprot_refseq);
@all_refseq = &nonRedundantList(\@all_refseq);
my $all_refseq=join(", ",@all_refseq);
	$result_str .= "RefSeq_ID: $all_refseq\n";
my $hgnc_entrezgene = $hgnc_annotation{Entrez_Gene_ID};
my @hgnc_entrezgene = split("__",$hgnc_entrezgene) if $hgnc_entrezgene;
my $uniprot_entrezgene = $uniprot_annotation{GeneID}; 
my @uniprot_entrezgene = split("__",$uniprot_entrezgene) if $uniprot_entrezgene;
my @all_entrezgene = (@uniprot_entrezgene, @uniprot_entrezgene);
@all_entrezgene = &nonRedundantList(\@all_entrezgene);
my $all_entrezgene=join(", ",@all_entrezgene);
	$result_str .= "EnrezGene_ID: $all_entrezgene\n";
my $hgnc_ensembl = $hgnc_annotation{Ensembl};
my @hgnc_ensembl = split("__",$hgnc_ensembl) if $hgnc_ensembl;
my $uniprot_ensembl = $uniprot_annotation{Ensembl}; 
my @uniprot_ensembl = split("__",$uniprot_ensembl) if $uniprot_ensembl;
my @all_ensembl = (@uniprot_ensembl, @uniprot_ensembl);
map(s/\.//g, @all_ensembl);
@all_ensembl = &nonRedundantList(\@all_ensembl);
my $all_ensembl=join(", ",@all_ensembl);
	$result_str .= "Ensembl_ID: $all_ensembl\n";
my $hgnc_ucsc = $hgnc_annotation{UCSC};
my @hgnc_ucsc = split("__",$hgnc_ucsc) if $hgnc_ucsc;
my $uniprot_ucsc = $uniprot_annotation{UCSC}; 
my @uniprot_ucsc = split("__",$uniprot_ucsc) if $uniprot_ucsc;
my @all_ucsc = (@uniprot_ucsc, @uniprot_ucsc);
@all_ucsc = &nonRedundantList(\@all_ucsc);
my $all_ucsc=join(", ",@all_ucsc);
	$result_str .= "UCSC_ID: $all_ucsc\n";
my $uniprot_reactome = $uniprot_annotation{Reactome}; 
my @uniprot_reactome = split("__",$uniprot_reactome) if $uniprot_reactome;
my $all_reactome=join(", ",@uniprot_reactome);
	$result_str .= "Reactome_ID: $all_reactome\n";
# next run add pubmed_ids to uniprot db_xref ......imp note
my $hgnc_pubmed = $hgnc_annotation{Pubmed_IDs};
my @hgnc_pubmed = split("__",$hgnc_pubmed) if $hgnc_pubmed;
#my $uniprot_pubmed = $uniprot_annotation{Pubmed_IDs}; 
#my @uniprot_pubmed = split("__",$uniprot_pubmed) if $uniprot_pubmed;
#my @all_pubmed = (@uniprot_pubmed, @uniprot_pubmed);
#@all_pubmed = &nonRedundantList(\@all_pubmed);
my $all_pubmed=join(", ",@hgnc_pubmed);
	$result_str .= "Pubmed_ID: $all_pubmed\n";
my $uniprot_embl = $uniprot_annotation{EMBL}; 
my @uniprot_embl = split("__",$uniprot_embl) if $uniprot_embl;
my $all_embl=join(", ",@uniprot_embl);
	$result_str .= "EMBL_ID: $all_embl\n";
my $uniprot_ipi = $uniprot_annotation{IPI}; 
my @uniprot_ipi = split("__",$uniprot_ipi) if $uniprot_ipi;
my $all_ipi=join(", ",@uniprot_ipi);
	$result_str .= "IPI_ID: $all_ipi\n";
my $uniprot_unigene = $uniprot_annotation{UniGene}; 
my @uniprot_unigene = split("__",$uniprot_unigene) if $uniprot_unigene;
my $all_unigene=join(", ",@uniprot_unigene);
	$result_str .= "UniGene_ID: $all_unigene\n";
my $uniprot_pdb = $uniprot_annotation{PDB}; 
my @uniprot_pdb = split("__",$uniprot_pdb) if $uniprot_pdb;
my $all_pdb=join(", ",@uniprot_pdb);
	$result_str .= "PDB_ID: $all_pdb\n";
my $uniprot_dip = $uniprot_annotation{DIP}; 
my @uniprot_dip = split("__",$uniprot_dip) if $uniprot_dip;
my $all_dip=join(", ",@uniprot_dip);
	$result_str .= "DIP_ID: $all_dip\n";
my $uniprot_mint = $uniprot_annotation{MINT}; 
my @uniprot_mint = split("__",$uniprot_mint) if $uniprot_mint;
my $all_mint=join(", ",@uniprot_mint);
	$result_str .= "MINT_ID: $all_mint\n";
my $uniprot_kegg = $uniprot_annotation{KEGG}; 
my @uniprot_kegg = split("__",$uniprot_kegg) if $uniprot_kegg;
my $all_kegg=join(", ",@uniprot_kegg);
	$result_str .= "KEGG_ID: $all_kegg\n";
my $uniprot_genecards = $uniprot_annotation{GeneCards}; 
my @uniprot_genecards = split("__",$uniprot_genecards) if $uniprot_genecards;
my $all_genecards=join(", ",@uniprot_genecards);
	$result_str .= "GeneCards_ID: $all_genecards\n";
#my $uniprot_hpa = $uniprot_annotation{HPA}; 
#my @uniprot_hpa = split("__",$uniprot_hpa) if $uniprot_hpa;
#my $all_hpa=join(", ",@uniprot_hpa);
#	$result_str .= "HPA_ID: $all_hpa\n";
my $uniprot_pharmagkb = $uniprot_annotation{PharmGKB}; 
my @uniprot_pharmagkb = split("__",$uniprot_pharmagkb) if $uniprot_pharmagkb;
my $all_pharmagkb=join(", ",@uniprot_pharmagkb);
	$result_str .= "PharmGKB_ID: $all_pharmagkb\n";
### ADD MIM, IntAct, H_invDB to uniprot dbxref
my $uniprot_pid = $uniprot_annotation{Pathway_Interaction_DB}; 
my @uniprot_pid = split("__",$uniprot_pid) if $uniprot_pid;
my $all_pid=join(", ",@uniprot_pid);
	$result_str .= "Pathway_Interaction_DB: $all_pid\n";
my $uniprot_go_f = $uniprot_annotation{GO_F}; 
my @uniprot_go_f = split("__",$uniprot_go_f) if $uniprot_go_f;
my $all_go_f=join(", ",@uniprot_go_f);
	$result_str .= "GO_Function: $all_go_f\n";
my $uniprot_go_p = $uniprot_annotation{GO_P}; 
my @uniprot_go_p = split("__",$uniprot_go_p) if $uniprot_go_p;
my $all_go_p=join(", ",@uniprot_go_p);
	$result_str .= "GO_Process: $all_go_p\n";
my $uniprot_go_c = $uniprot_annotation{GO_C}; 
my @uniprot_go_c = split("__",$uniprot_go_c) if $uniprot_go_c;
my $all_go_c=join(", ",@uniprot_go_c);
	$result_str .= "GO_Component: $all_go_c\n";
my $uniprot_interpro = $uniprot_annotation{InterPro}; 
my @uniprot_interpro = split("__",$uniprot_interpro) if $uniprot_interpro;
my $all_interpro=join(", ",@uniprot_interpro);
	$result_str .= "InterPro: $all_interpro\n";
my $uniprot_pfam = $uniprot_annotation{Pfam}; 
my @uniprot_pfam = split("__",$uniprot_pfam) if $uniprot_pfam;
my $all_pfam=join(", ",@uniprot_pfam);
	$result_str .= "Pfam: $all_pfam\n";
my $uniprot_panther = $uniprot_annotation{PANTHER}; 
my @uniprot_panther = split("__",$uniprot_panther) if $uniprot_panther;
my $all_panther=join(", ",@uniprot_panther);
	$result_str .= "PANTHER: $all_panther\n";
my $uniprot_hovergen = $uniprot_annotation{HOVERGEN}; 
my @uniprot_hovergen = split("__",$uniprot_hovergen) if $uniprot_hovergen;
my $all_hovergen=join(", ",@uniprot_hovergen);
	$result_str .= "HOVERGEN: $all_hovergen\n";

	return $result_str;
} #sub annotation_view {


sub nonRedundantList{
  my $val = shift;
  my @val=@$val;
  my %cpt;
  foreach (@val){
    $cpt{$_}++;
  }
  return keys %cpt;
} # sub redundantList{

1;
