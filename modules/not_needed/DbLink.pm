package DbLink;

use DbSession;
use Carp;

use base DeepPrintable;

sub GeneListSize {
  my ($tmp_database, $tmp_table, $org) = @_;
  my $size = 0;
  my $databaseHandle = DbSession::GetConnection();
  my $query = "";
  if ($org eq 'human') {
	    $query = "SELECT COUNT(*) FROM $tmp_database.$tmp_table";
  }
  elsif($org eq 'mouse') {
    $query = "SELECT COUNT(*) FROM $tmp_database.$tmp_table";
  }
  elsif($org eq 'yeast') {
    $query = "SELECT COUNT(*) FROM $tmp_database.$tmp_table";
  }
  #my $select = $databaseHandle->prepare($query);
  #$select->execute();
  my $select = $databaseHandle->prepare($query) or die "unable to prepare query : $query" . $databaseHandle->errstr;
  $select->execute() or die "unable to execute" . $databaseHandle->errstr;
	$size = $select->fetchrow_array();
  return $size;
} # sub GeneListSize { 

sub GetProteinsForGeneList {
	my ($tmp_database, $tmp_table, $org) = @_;
	my @proteinIds = ();
	my $databaseHandle = DbSession::GetConnection();
	my $query = "";
	if ($org eq 'human') {
		$query = "SELECT DISTINCT b.longest_protein FROM biocompendium.human_gene_protein b, $tmp_database.$tmp_table t where t.gene=b.gene";
	}
	elsif($org eq 'mouse') {
		$query = "SELECT DISTINCT b.longest_protein FROM biocompendium.mouse_gene_protein b, $tmp_database.$tmp_table t where t.gene=b.gene";
	}
	elsif($org eq 'yeast') {
		$query = "SELECT DISTINCT b.longest_protein FROM biocompendium.yeast_gene_protein b, $tmp_database.$tmp_table t where t.gene=b.gene";
	}
#	my $select = $databaseHandle->prepare($query);
#	$select->execute();
  my $select = $databaseHandle->prepare($query) or die "unable to prepare query : $query" . $databaseHandle->errstr;
  $select->execute() or die "unable to execute" . $databaseHandle->errstr;
	my $nr = $select->rows();
	while ($nr--) {
		push @proteinIds, $select->fetchrow_array();
	} # while ($nr--) {
	return @proteinIds;
} # sub GetProteinsForGeneList {


sub GetOrthologyIdsForGeneList {
	my ($tmp_database, $tmp_table, $org) = @_;
	my @orthologyIds = ();
	my $databaseHandle = DbSession::GetConnection();
	my $query = "";
	if ($org eq 'human') {
		$query = "SELECT DISTINCT bo.id FROM biocompendium.human_orthology bo, biocompendium.human_gene_protein bgp, $tmp_database.$tmp_table t WHERE  bo.orthologs_details !=bgp.gene_dbid  AND t.gene=bgp.gene AND bgp.longest_protein=bo.protein";
	}
	elsif($org eq 'mouse') {
		$query = "SELECT DISTINCT bo.id FROM biocompendium.mouse_orthology bo, biocompendium.mouse_gene_protein bgp, $tmp_database.$tmp_table t WHERE  bo.orthologs_details !=bgp.gene_dbid  AND t.gene=bgp.gene AND bgp.longest_protein=bo.protein";
	}
	elsif($org eq 'yeast') {
		$query = "SELECT DISTINCT bo.id FROM biocompendium.yeast_orthology bo, biocompendium.yeast_gene_protein bgp, $tmp_database.$tmp_table t WHERE  bo.orthologs_details !=bgp.gene_dbid  AND t.gene=bgp.gene AND bgp.longest_protein=bo.protein";
	}
#	my $select = $databaseHandle->prepare($query);
#	$select->execute();
  my $select = $databaseHandle->prepare($query) or die "unable to prepare query : $query" . $databaseHandle->errstr;
  $select->execute() or die "unable to execute" . $databaseHandle->errstr;
	my $nr = $select->rows();
	while ($nr--) {
		push @orthologyIds, $select->fetchrow_array();
	} # while ($nr--) {
	return @orthologyIds;
} # sub GetOrthologyIdsForGeneList

sub GetDiseaseForGene {
	my ($gene, $org) = @_;
	my %disease_hash = ();
	my $databaseHandle = DbSession::GetConnection();
	my $query = "";
	if ($org eq 'human') {
    $query = "SELECT * FROM biocompendium.human_diseases WHERE gene=?";
	}
#	elsif($org eq 'mouse') {
#		$query = "SELECT * FROM biocompendium.mouse_diseases WHERE gene=?;";
#	}
#	elsif($org eq 'yeast') {
#		$query = "SELECT * FROM biocompendium.yeast_diseases WHERE gene=?;";
#	}
#	my $select = $databaseHandle->prepare("$query");
#	$select->execute($gene);
  my $select = $databaseHandle->prepare($query) or die "unable to prepare query : $query" . $databaseHandle->errstr;
  $select->execute($gene) or die "unable to execute" . $databaseHandle->errstr;
	my $nr = $select->rows();
#print "nr : $nr\n";
	my @data;
	while ($nr--) {
	     	@data = $select->fetchrow_array();
		my $id = $data[0];
		my $gene = $data[1];
		my $mim_morbid_acc = $data[2];
		my $description = $data[3];
		$disease_hash{$mim_morbid_acc}{description} = $description;
	}
	\%disease_hash;
} # sub GetDiseaseForGene {

sub GetKeggForGene {
	my ($gene, $org) = @_;
	my %kegg_hash = ();
	my $databaseHandle = DbSession::GetConnection();
	my $query = "";
	if ($org eq 'human') {
    $query = "SELECT * FROM biocompendium.human_pathway_kegg2 WHERE gene=?";
	}
	elsif($org eq 'mouse') {
		$query = "SELECT * FROM biocompendium.mouse_pathway_kegg2 WHERE gene=?;";
	}
	elsif($org eq 'yeast') {
		$query = "SELECT * FROM biocompendium.yeast_pathway_kegg2 WHERE gene=?;";
	}
#	my $select = $databaseHandle->prepare("$query");
#	$select->execute($gene);
  my $select = $databaseHandle->prepare($query) or die "unable to prepare query : $query" . $databaseHandle->errstr;
  $select->execute($gene) or die "unable to execute" . $databaseHandle->errstr;
	my $nr = $select->rows();
#print "nr : $nr\n";
	my @data;
	while ($nr--) {
	     	@data = $select->fetchrow_array();
		my $id = $data[0];
		my $gene = $data[1];
		my $kegg_id = $data[2];
		my $pathway_description = $data[3];
		my $kegg_gene = $data[4];
		$kegg_hash{$kegg_id}{pathway_description} = $pathway_description;
		$kegg_hash{$kegg_id}{kegg_gene} = $kegg_gene;
	}
	\%kegg_hash;
} # sub GetKeggForGene {

sub GetKegg {
	my ($tmp_database, $tmp_table, $org) = @_;
	my %kegg_hash = ();
	my %kegg_detail_hash = ();
	my $databaseHandle = DbSession::GetConnection();
	my $query = "";
	if ($org eq 'human') {
#    $query = "SELECT DISTINCT k.*, g.name FROM biocompendium.human_pathway_kegg k, biocompendium.human_gene_name g, $tmp_database.$tmp_table t WHERE t.gene=k.gene AND t.gene=g.gene ORDER BY k.id;";
    $query = "SELECT DISTINCT k.* FROM biocompendium.human_pathway_kegg2 k, $tmp_database.$tmp_table t WHERE t.gene=k.gene ORDER BY k.id;";
	}
	elsif($org eq 'mouse') {
#		$query = "SELECT DISTINCT k.*, g.name FROM biocompendium.mouse_pathway_kegg k, biocompendium.mouse_gene_name g, $tmp_database.$tmp_table t WHERE t.gene=k.gene AND t.gene=g.gene ORDER BY k.id;";
		$query = "SELECT DISTINCT k.* FROM biocompendium.mouse_pathway_kegg2 k, $tmp_database.$tmp_table t WHERE t.gene=k.gene ORDER BY k.id;";
	}
	elsif($org eq 'yeast') {
#		$query = "SELECT DISTINCT k.*, g.name FROM biocompendium.yeast_pathway_kegg k, biocompendium.yeast_gene_name g, $tmp_database.$tmp_table t WHERE t.gene=k.gene AND t.gene=g.gene ORDER BY k.id;";
		$query = "SELECT DISTINCT k.* FROM biocompendium.yeast_pathway_kegg2 k, $tmp_database.$tmp_table t WHERE t.gene=k.gene ORDER BY k.id;";
	}
#	my $select = $databaseHandle->prepare("$query");
#	$select->execute();
  my $select = $databaseHandle->prepare($query) or die "unable to prepare query : $query" . $databaseHandle->errstr;
  $select->execute() or die "unable to execute" . $databaseHandle->errstr;
	my $nr = $select->rows();
#print "nr : $nr\n";
	my @data;
	while ($nr--) {
	     	@data = $select->fetchrow_array();
		my $id = $data[0];
		my $gene = $data[1];
		my $kegg_id = $data[2];
		my $pathway_description = $data[3];
		my $kegg_gene = $data[4];
		my $name = $data[5];
		$kegg_detail_hash{$id}{id} = $id;
		$kegg_detail_hash{$id}{gene} = $gene;
		$kegg_detail_hash{$id}{kegg_id} = $kegg_id;
		$kegg_detail_hash{$id}{pathway_description} = $pathway_description;
		$kegg_detail_hash{$id}{kegg_gene} = $kegg_gene;
		$kegg_detail_hash{$id}{name} = $name;

		push @{$kegg_hash{$kegg_id}}, $id;
	}
	my %kegg_result = (kegg_hash=>\%kegg_hash, kegg_detail_hash=>\%kegg_detail_hash);
	\%kegg_result;
} # sub GetKegg {

sub GetPatentDetails {
  my ($org, $protein, $cut_off) = @_;
	my %patent_hash = ();
	my %patent_detail_hash = ();
  my $databaseHandle = DbSession::GetConnection();
  my $query = "";
  if ($org eq 'human') {
	  $query = "SELECT DISTINCT  PAT.*, PATA.* FROM biocompendium.human_patent PAT, biocompendium.human_patent_annotation PATA WHERE PAT.protein=? AND PATA.tax_id=9606 AND PAT.patent_id=PATA.patent_id ORDER BY PAT.frac_identical DESC;";
  }
  elsif($org eq 'mouse') {
	  $query = "SELECT DISTINCT  PAT.*, PATA.* FROM biocompendium.mouse_patent PAT, biocompendium.mouse_patent_annotation PATA WHERE PAT.protein=? AND PATA.tax_id=10090 AND PAT.patent_id=PATA.patent_id ORDER BY PAT.frac_identical DESC;";
  }
  elsif($org eq 'yeast') {
	  $query = "SELECT DISTINCT  PAT.*, PATA.* FROM biocompendium.yeast_patent PAT, biocompendium.yeast_patent_annotation PATA WHERE PAT.protein=? AND PATA.tax_id=4932 AND PAT.patent_id=PATA.patent_id ORDER BY PAT.frac_identical DESC;";
  }
#print "query : $query<br>";	
#  my $select = $databaseHandle->prepare("$query");
#  $select->execute($protein);
  my $select = $databaseHandle->prepare($query) or die "unable to prepare query : $query" . $databaseHandle->errstr;
  $select->execute($protein) or die "unable to execute" . $databaseHandle->errstr;
  my $nr = $select->rows();
#print "nr : $nr\n";
  my @data;
  while ($nr--) {
        @data = $select->fetchrow_array();
#data from  human_patent (hp)		
    my $hp__id              = $data[0];
    my $patent_id       = $data[1];
    my $hp__protein         = $data[2];
    my $hp__significance    = $data[3];
    my $hp__score           = $data[4];
    my $hp__frac_identical  = $data[5];
    my $hp__hssps           = $data[6];
# data from human_patent_annotation (hpa)		
    my $hpa__id             = $data[7];
    my $hpa__patent_id      = $data[8];
    my $hpa__patent_office  = $data[9];
    my $hpa__nr_id          = $data[10];
    my $hpa__mf             = $data[11];
    my $hpa__des            = $data[12];
    my $hpa__patent_from_de = $data[13];
    my $hpa__seq_len        = $data[14];
    my $hpa__md5            = $data[15];
    my $hpa__org            = $data[16];
    my $hpa__mol_type       = $data[17];
    my $hpa__tax_id         = $data[18];
    my $hpa__note           = $data[19];
    my $hpa__title          = $data[20];
		if ($hp__frac_identical >= $cut_off) { 
	    $patent_detail_hash{$patent_id}{patent_id} = $patent_id;
	    $patent_detail_hash{$patent_id}{frac_identical} = $hp__frac_identical;
	    $patent_detail_hash{$patent_id}{hssps} = $hp__hssps;
	    $patent_detail_hash{$patent_id}{patent_office} = $hpa__patent_office;
	    $patent_detail_hash{$patent_id}{nr_id} = $hpa__nr_id;
	    $patent_detail_hash{$patent_id}{mf} = $hpa__mf;
	    $patent_detail_hash{$patent_id}{des} = $hpa__des;
	    $patent_detail_hash{$patent_id}{patent_from_de} = $hpa__patent_from_de;
	    $patent_detail_hash{$patent_id}{seq_len} = $hpa__seq_len;
	    $patent_detail_hash{$patent_id}{md5} = $hpa__md5;
	    $patent_detail_hash{$patent_id}{mol_type} = $hpa__mol_type;
	    $patent_detail_hash{$patent_id}{note} = $hpa__note;
	    $patent_detail_hash{$patent_id}{title} = $hpa__title;

	    $patent_hash{$patent_id} = $hp__frac_identical;
		}
  }
  my %patent_result = (patent_hash=>\%patent_hash, patent_detail_hash=>\%patent_detail_hash);
  \%patent_result;
} # sub GetPatentDetails {

sub GetPatent {
  my ($tmp_database, $tmp_table, $org, $cut_off) = @_;
  my %patent_hash = ();
  my $databaseHandle = DbSession::GetConnection();
  my $query = "";
  if ($org eq 'human') {
		$query = "SELECT DISTINCT BHGP.gene, PAT.protein,BHGN.name, BHGP.description FROM biocompendium.human_patent PAT, biocompendium.human_gene_name BHGN, biocompendium.human_gene_protein BHGP, $tmp_database.$tmp_table TMP WHERE TMP.gene=BHGP.gene AND PAT.protein=BHGP.longest_protein AND TMP.gene=BHGN.gene AND PAT.frac_identical >=$cut_off  ORDER BY PAT.frac_identical DESC;";
  }
  elsif($org eq 'mouse') {
		$query = "SELECT DISTINCT BHGP.gene, PAT.protein,BHGN.name, BHGP.description FROM biocompendium.mouse_patent PAT, biocompendium.mouse_gene_name BHGN, biocompendium.mouse_gene_protein BHGP, $tmp_database.$tmp_table TMP WHERE TMP.gene=BHGP.gene AND PAT.protein=BHGP.longest_protein AND TMP.gene=BHGN.gene AND PAT.frac_identical >=$cut_off ORDER BY PAT.frac_identical DESC;";
  }
  elsif($org eq 'yeast') {
		 $query = "SELECT DISTINCT BHGP.gene, PAT.protein,BHGN.name, BHGP.description FROM biocompendium.yeast_patent PAT, biocompendium.yeast_gene_name BHGN, biocompendium.yeast_gene_protein BHGP, $tmp_database.$tmp_table TMP WHERE TMP.gene=BHGP.gene AND PAT.protein=BHGP.longest_protein AND TMP.gene=BHGN.gene AND PAT.frac_identical >=$cut_off ORDER BY PAT.frac_identical DESC;";
  }
#  my $select = $databaseHandle->prepare("$query");
#  $select->execute();
  my $select = $databaseHandle->prepare($query) or die "unable to prepare query : $query" . $databaseHandle->errstr;
  $select->execute() or die "unable to execute" . $databaseHandle->errstr;
  my $nr = $select->rows();
#print "nr : $nr\n";
  my @data;
  while ($nr--) {
        @data = $select->fetchrow_array();
    my $ens_gene            = $data[0];
    my $ens_protein         = $data[1];
    my $name           = $data[2];
    my $des           = $data[3];

	    $patent_hash{$ens_gene}{ens_protein} = $ens_protein;
	    $patent_hash{$ens_gene}{name} = $name;
	    $patent_hash{$ens_gene}{des} = $des;
  }
  \%patent_hash;
} # sub GetPatent {

sub GetTFBS {
	my ($tmp_database, $tmp_table, $org) = @_;
	my %tfbs_hash = ();
	my $databaseHandle = DbSession::GetConnection();
  my $query = "";
  if ($org eq 'human') {
		$query = "SELECT DISTINCT TFBS.gene, TFBS.tfbs_line, BHGN.name from biocompendium.human_tfbs TFBS, biocompendium.human_gene_name BHGN, $tmp_database.$tmp_table TMP WHERE TFBS.gene=TMP.gene AND TFBS.gene=BHGN.gene;";
	}
	elsif($org eq 'mouse') {
		$query = "SELECT DISTINCT TFBS.gene, TFBS.tfbs_line, BHGN.name from biocompendium.mouse_tfbs TFBS, biocompendium.mouse_gene_name BHGN, $tmp_database.$tmp_table TMP WHERE TFBS.gene=TMP.gene AND TFBS.gene=BHGN.gene;";
	}
#	my $select = $databaseHandle->prepare("$query");
#	$select->execute();
  my $select = $databaseHandle->prepare($query) or die "unable to prepare query : $query" . $databaseHandle->errstr;
  $select->execute() or die "unable to execute" . $databaseHandle->errstr;
  my $nr = $select->rows();
  my @data;
  while ($nr--) {
    @data = $select->fetchrow_array();
    my $gene      = $data[0];
    my $tfbs_line = $data[1];
    my $name      = $data[2];

      $tfbs_hash{$gene}{tfbs_line} = $tfbs_line;
      $tfbs_hash{$gene}{name} = $name;
  }
  \%tfbs_hash;
} # sub GetTFBS {

sub GetHumanProteinAtlasIdForGene {
  my ($gene, $org) = @_;
  my @hpa_ids = ();
  my $databaseHandle = DbSession::GetConnection();
  my $query = "";
  if ($org eq 'human') {
    $query = "SELECT DISTINCT hpa_id FROM biocompendium.human_protein_atlas WHERE gene=?";
  }
# elsif($org eq 'mouse') {
# }
# elsif($org eq 'yeast') {
# }
#  my $select = $databaseHandle->prepare("$query");
#  $select->execute($gene);
  my $select = $databaseHandle->prepare($query) or die "unable to prepare query : $query" . $databaseHandle->errstr;
  $select->execute($gene) or die "unable to execute" . $databaseHandle->errstr;
  my $nr = $select->rows();
#print "nr : $nr\n";
  my @data;
  while ($nr--) {
		@data = $select->fetchrow_array();
    my $hpa_id = $data[0];
		push @hpa_ids, $hpa_id;
  }
  @hpa_ids;
} # sub GetHumanProteinAtlasIdForGene {

sub GetDescriptionForProtein {
	my ($protein, $org) = @_;
	my $des = ();
	my $databaseHandle = DbSession::GetConnection();
	my $query = "";
	if ($org eq 'human') {
    $query = "SELECT description FROM human_gene_protein WHERE longest_protein=?";
	}
	elsif($org eq 'mouse') {
		$query = "SELECT description FROM mouse_gene_protein WHERE longest_protein=?;";
	}
	elsif($org eq 'yeast') {
		$query = "SELECT description FROM yeast_gene_protein WHERE longest_protein=?;";
	}
	elsif($org eq 'fish') {
		$query = "SELECT description FROM fish_gene_protein WHERE longest_protein=?;";
	}
	elsif($org eq 'fly') {
		$query = "SELECT description FROM fly_gene_protein WHERE longest_protein=?;";
	}
	elsif($org eq 'rat') {
		$query = "SELECT description FROM rat_gene_protein WHERE longest_protein=?;";
	}
	elsif($org eq 'worm') {
		$query = "SELECT description FROM worm_gene_protein WHERE longest_protein=?;";
	}
#	my $select = $databaseHandle->prepare("$query");
#	$select->execute($protein);
  my $select = $databaseHandle->prepare($query) or die "unable to prepare query : $query" . $databaseHandle->errstr;
  $select->execute($protein) or die "unable to execute" . $databaseHandle->errstr;
	$des = $select->fetchrow_array();
	return $des;
} # sub GetDescriptionForProtein {
1;
