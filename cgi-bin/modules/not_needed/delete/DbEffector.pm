package DbEffector;

##########################################
##
## Document   : DbEffector.pm
## Created on : June 25th, 2009
## Author     : Venkata P. Satagopam (venkata.satagopam@embl.de)
##
##########################################

use DbSessionGpdb;
use Carp;

use base DeepPrintable;

use constant LOAD_STATEMENT => "SELECT * FROM effector WHERE id=?";

sub GetDistinctFamily {
        my @effector_family = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT DISTINCT(family) FROM effector");
        $select->execute();
        my $nr = $select->rows();
        while ($nr--) {
            push @effector_family, $select->fetchrow_array();
        }
   @effector_family;
} # sub GetDistinctFamily {

sub GetSubfamilyForFamily {
        my $family = shift;
        my @effector_subfamily = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT DISTINCT(subfamily) FROM effector WHERE family=?");
        $select->execute($family);
        my $nr = $select->rows();
        while ($nr--) {
            push @effector_subfamily, $select->fetchrow_array();
        }
   @effector_subfamily;
} # sub GetSubfamilyForClassAndFamily {

sub GetTypeForFamilyAndSubfamily {
        my $family = shift;
        my $subfamily = shift;
        my @effector_type = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT DISTINCT(type) FROM effector WHERE family=? AND subfamily=?");
        $select->execute($family, $subfamily);
        my $nr = $select->rows();
        while ($nr--) {
            push @effector_type, $select->fetchrow_array();
        }
   @effector_type;
} # sub GetTypeForClassAndFamilyAndSubfamily {

sub GetIdsForFamilyAndSubfamilyAndType {
        my $family = shift;
        my $subfamily = shift;
        my $type = shift;
        my @effector_ids = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT DISTINCT(id) FROM effector WHERE family=? AND subfamily=? AND type=?");
        $select->execute($family, $subfamily, $type);
        my $nr = $select->rows();
        while ($nr--) {
            push @effector_ids, $select->fetchrow_array();
        }
   @effector_ids;
} # sub GetIdsForFamilyAndSubfamilyAndType {

sub GetSubfamily {
        my ($level, $node) = @_;
        my @effector_subfamily = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $query = "";
        if ($level eq 'top') {
                $query = "SELECT DISTINCT(subfamily) FROM effector";
        }
        elsif($level eq 'family') {
                $query = "SELECT DISTINCT(subfamily) FROM effector WHERE family=\"$node\"";
        }
        elsif($level eq 'subfamily') {
                $query = "SELECT DISTINCT(subfamily) FROM effector WHERE subfamily=\"$node\"";
        }
        elsif($level eq 'type') {
                $query = "SELECT DISTINCT(subfamily) FROM effector WHERE type=\"$node\"";
        }
        my $select = $databaseHandle->prepare("$query");
        $select->execute();
        my $nr = $select->rows();

        while ($nr--) {
            push @effector_subfamily, $select->fetchrow_array();
        }
   @effector_subfamily;
} # sub GetSubfamily {

sub GetIds {
        my ($level, $node, $sort_by_field_name, $asc_or_desc) = @_;
        my @effector_ids = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $query = "";
        if ($level eq 'top') {
                $query = "SELECT DISTINCT(id) FROM effector ORDER BY $sort_by_field_name $asc_or_desc";
        }
        elsif($level eq 'family') {
                $query = "SELECT DISTINCT(id) FROM effector WHERE family=\"$node\" ORDER BY $sort_by_field_name $asc_or_desc";
        }
        elsif($level eq 'subfamily') {
                $query = "SELECT DISTINCT(id) FROM effector WHERE subfamily=\"$node\" ORDER BY $sort_by_field_name $asc_or_desc";
        }
        elsif($level eq 'type') {
                $query = "SELECT DISTINCT(id) FROM effector WHERE type=\"$node\" ORDER BY $sort_by_field_name $asc_or_desc";
        }
        my $select = $databaseHandle->prepare("$query");
        $select->execute();
        my $nr = $select->rows();
        while ($nr--) {
            push @effector_ids, $select->fetchrow_array();
        }
   @effector_ids;
} # sub GetIds {

sub GetKegg {
        my ($level, $node) = @_;
        my %kegg_hash = ();
        my %kegg_detail_hash = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $query = "";
        if ($level eq 'top') {
                $query = "SELECT DISTINCT k.*, e.sp_pir_id, e.sp_acc, e.name FROM eff_pathway_kegg k, effector e, eff_validation v WHERE e.sp_pir_id=v.sp_pir_id AND v.ensembl_gene=k.gene ORDER BY k.id;";
        }
        elsif($level eq 'family') {
                $query = "SELECT DISTINCT k.*, e.sp_pir_id, e.sp_acc, e.name FROM eff_pathway_kegg k, effector e, eff_validation v WHERE e.family=\"$node\" AND e.sp_pir_id=v.sp_pir_id AND v.ensembl_gene=k.gene ORDER BY k.id;";
        }
        elsif($level eq 'subfamily') {
                $query = "SELECT DISTINCT k.*, e.sp_pir_id, e.sp_acc, e.name FROM eff_pathway_kegg k, effector e, eff_validation v WHERE e.subfamily=\"$node\" AND e.sp_pir_id=v.sp_pir_id AND v.ensembl_gene=k.gene ORDER BY k.id;";
        }
        elsif($level eq 'type') {
                $query = "SELECT DISTINCT k.*, e.sp_pir_id, e.sp_acc, e.name FROM eff_pathway_kegg k, effector e, eff_validation v WHERE e.type=\"$node\" AND e.sp_pir_id=v.sp_pir_id AND v.ensembl_gene=k.gene ORDER BY k.id;";
        }
        my $select = $databaseHandle->prepare("$query");
        $select->execute();
        my $nr = $select->rows();
	my @data;
        while ($nr--) {
             	@data = $select->fetchrow_array();
		my $id = $data[0];
		my $gene = $data[1];
		my $kegg_id = $data[2];
		my $pathway_description = $data[3];
		my $kegg_gene = $data[4];
		my $sp_pir_id = $data[5];
		my $sp_acc = $data[6];
		my $name = $data[7];
		$kegg_detail_hash{$sp_pir_id}{id} = $id;
		$kegg_detail_hash{$sp_pir_id}{gene} = $gene;
		$kegg_detail_hash{$sp_pir_id}{kegg_id} = $kegg_id;
		$kegg_detail_hash{$sp_pir_id}{pathway_description} = $pathway_description;
		$kegg_detail_hash{$sp_pir_id}{kegg_gene} = $kegg_gene;
		$kegg_detail_hash{$sp_pir_id}{sp_pir_id} = $sp_pir_id;
		$kegg_detail_hash{$sp_pir_id}{sp_acc} = $sp_acc;
		$kegg_detail_hash{$sp_pir_id}{name} = $name;

		push @{$kegg_hash{$kegg_id}}, $sp_pir_id;
        }
	my %kegg_result = (kegg_hash=>\%kegg_hash, kegg_detail_hash=>\%kegg_detail_hash);
	\%kegg_result;
} # sub GetKegg {

sub GetEnsemblProteins{
        my ($level, $node) = @_;
        my @ensp = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $query = "";
        if ($level eq 'top') {
                $query = " SELECT DISTINCT s.longest_protein from eff_gene_protein s, effector e, eff_validation v WHERE e.sp_pir_id=v.sp_pir_id AND v.ensembl_gene=s.gene;";
        }
        elsif($level eq 'family') {
                $query = " SELECT DISTINCT s.longest_protein from eff_gene_protein s, effector e, eff_validation v WHERE e.family=\"$node\" AND e.sp_pir_id=v.sp_pir_id AND v.ensembl_gene=s.gene;";
        }
        elsif($level eq 'subfamily') {
                $query = " SELECT DISTINCT s.longest_protein from eff_gene_protein s, effector e, eff_validation v WHERE e.subfamily=\"$node\" AND e.sp_pir_id=v.sp_pir_id AND v.ensembl_gene=s.gene;";
        }
        elsif($level eq 'type') {
                $query = " SELECT DISTINCT s.longest_protein from eff_gene_protein s, effector e, eff_validation v WHERE e.type=\"$node\" AND e.sp_pir_id=v.sp_pir_id AND v.ensembl_gene=s.gene;";
        }
        my $select = $databaseHandle->prepare("$query");
        $select->execute();
        my $nr = $select->rows();
        while ($nr--) {
		push @ensp, $select->fetchrow_array();
        }
	@ensp;
} # sub GetEnsemblProteins{

sub GetNameForProtein {
        my $longest_protein = shift;
        my $name = "";
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT e.name FROM eff_gene_protein s, effector e, eff_validation v WHERE s.longest_protein=? AND e.sp_pir_id=v.sp_pir_id AND v.ensembl_gene=s.gene");
        $select->execute($longest_protein);
        $name = $select->fetchrow_array();
        $name;
} # sub GetNameForProtein {


sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{id} = 0;
    $this->{name} =''; 
    $this->{sp_pir_id} = '';
    $this->{sp_acc} = '';
    $this->{fragment} = '';
    $this->{family} = '';
    $this->{subfamily} = '';
    $this->{type} = '';
    $this->{description} = '';
    $this->{gene} = '';
    $this->{common_name} = '';
    $this->{species} = '';
    $this->{ncbi_taxid} = 0;
    $this->{function} = 0;
    $this->{embl} = '';
    $this->{pir} = '';
    $this->{pdb} = '';
    $this->{hssp} = '';
    $this->{geneid} = '';
    $this->{mim} = '';
    $this->{mgi} = '';
    $this->{wormpep} = '';
    $this->{flybase} = '';
    $this->{interpro} = '';
    $this->{pfam} = '';
    $this->{prints} = '';
    $this->{prodom} = '';
    $this->{smart} = '';
    $this->{seq} = '';

    $this->_initialize(@_);
    $this;
}

sub _initialize {
    my $this = shift;
    my $id = shift;

    if ($id) {
	my $databaseHandle = DbSessionGpdb::GetConnection();
	my $select = $databaseHandle->prepare(LOAD_STATEMENT);
	$select->execute($id);
	if ($select->rows == 1) {
		my @attr = $select->fetchrow_array;
		$this->{id} = shift @attr;
		$this->{name} = shift @attr;
		$this->{sp_pir_id} = shift @attr;
		$this->{sp_acc} = shift @attr;
		$this->{fragment} = shift @attr;
		$this->{family} = shift @attr;
		$this->{subfamily} = shift @attr;
		$this->{type} = shift @attr;
		$this->{description} = shift @attr;
		$this->{gene} = shift @attr;
		$this->{common_name} = shift @attr;
		$this->{species} = shift @attr;
		$this->{ncbi_taxid} = shift @attr;
		$this->{function} = shift @attr;
		$this->{embl} = shift @attr;
		$this->{pir} = shift @attr;
		$this->{pdb} = shift @attr;
		$this->{hssp} = shift @attr;
		$this->{geneid} = shift @attr;
		$this->{mim} = shift @attr;
		$this->{mgi} = shift @attr;
		$this->{wormpep} = shift @attr;
		$this->{flybase} = shift @attr;
		$this->{interpro} = shift @attr;
		$this->{pfam} = shift @attr;
		$this->{prints} = shift @attr;
		$this->{prodom} = shift @attr;
		$this->{smart} = shift @attr;
		$this->{seq} = shift @attr;
	} else {
	    carp "Initializing effector : unexpected number of records = ",$select->rows,"\n";
	}
    }
}


1;
