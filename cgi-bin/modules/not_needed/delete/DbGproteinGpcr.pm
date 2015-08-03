package DbGproteinGpcr;

##########################################
##
## Document   : DbGproteinGpcr.pm
## Created on : June 25th, 2009
## Author     : Venkata P. Satagopam (venkata.satagopam@embl.de)
##
##########################################

use DbSessionGpdb;
use Carp;

use base DeepPrintable;

use constant LOAD_STATEMENT => "SELECT * FROM gprotein_gpcr WHERE id=?";


sub GetGpcrIdsForGproteinId {
	my $gprotein_id = shift;
	my @gpcr_ids = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT DISTINCT(r.id) FROM gprotein_gpcr gg, gpcr r, gprotein g WHERE g.id=? AND gg.coupling !=\"\" AND gg.gpcr_sub=r.gpcr_sub AND gg.coupling=g.coupling");
        $select->execute($gprotein_id);
	my $nr = $select->rows();
        while ($nr--) {
            push @gpcr_ids, $select->fetchrow_array();
        }
   @gpcr_ids;	
} # sub GetGpcrIdsForGproteinId {

sub GetGpcrDetailsForGproteinId {
        my $gprotein_id = shift;
        my %gpcr_details_hash = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT DISTINCT(r.id), r.name, gg.coupling, gg.pubmed FROM gprotein_gpcr gg, gpcr r, gprotein g WHERE g.id=? AND gg.coupling !=\"\" AND gg.gpcr_sub=r.gpcr_sub AND gg.coupling=g.coupling");
        $select->execute($gprotein_id);
        my $nr = $select->rows();
	my @data;
        while ($nr--) {
                @data = $select->fetchrow_array();
                my $id = $data[0];
                my $name = $data[1];
                my $coupling = $data[2];
                my $pubmed = $data[3];
                $gpcr_details_hash{$id}{name} = $name;
                $gpcr_details_hash{$id}{coupling} = $coupling;
                $gpcr_details_hash{$id}{pubmed} = $pubmed;
        }
   \%gpcr_details_hash;
} # sub GetGpcrDetailsForGproteinId {

sub GetGproteinIdsForGpcrId {
        my $gpcr_id = shift;
        my @gprotein_ids = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT DISTINCT(g.id) FROM gprotein_gpcr gg, gprotein g, gpcr r WHERE r.id=? AND gg.coupling !=\"\" AND gg.coupling=g.coupling AND r.gpcr_sub=gg.gpcr_sub");
        $select->execute($gpcr_id);
        my $nr = $select->rows();
        while ($nr--) {
            push @gprotein_ids, $select->fetchrow_array();
        }
   @gprotein_ids;
} # sub GetGproteinIdsForGpcrId {

sub GetGproteinDetailsForGpcrId {
        my $gpcr_id = shift;
        my %gprotein_details_hash = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT DISTINCT(g.id), g.name, gg.coupling, gg.pubmed  FROM gprotein_gpcr gg, gprotein g, gpcr r WHERE r.id=? AND gg.coupling !=\"\" AND gg.coupling=g.coupling AND r.gpcr_sub=gg.gpcr_sub");
        $select->execute($gpcr_id);
        my $nr = $select->rows();
	my @data;
        while ($nr--) {
                @data = $select->fetchrow_array();
                my $id = $data[0];
                my $name = $data[1];
                my $coupling = $data[2];
                my $pubmed = $data[3];
                $gprotein_details_hash{$id}{name} = $name;
                $gprotein_details_hash{$id}{coupling} = $coupling;
                $gprotein_details_hash{$id}{pubmed} = $pubmed;
        }
   \%gprotein_details_hash;
} # sub GetGproteinDetailsForGpcrId {

sub GetGproteinSubForGpcrSub {
        my $gpcr_subfamily = shift;
        my @gprotein_subfamily = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT DISTINCT(g.subfamily) FROM gprotein_gpcr gg, gprotein g WHERE gg.gpcr_sub=? AND gg.coupling !=\"\" AND gg.coupling=g.coupling");
        $select->execute($gpcr_subfamily);
        my $nr = $select->rows();
        while ($nr--) { 
            push @gprotein_subfamily, $select->fetchrow_array();
        }
   @gprotein_subfamily;
} # sub GetGproteinSubForGpcrSub {

sub GetGpcrSubForGproteinSub {
        my $gprotein_subfamily = shift;
        my @gpcr_subfamily = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT DISTINCT(r.gpcr_sub) FROM gprotein_gpcr gg, gprotein g, gpcr r WHERE g.subfamily=? AND gg.coupling !=\"\" AND gg.coupling=g.coupling AND r.gpcr_sub=gg.gpcr_sub");
        $select->execute($gprotein_subfamily);
        my $nr = $select->rows();
        while ($nr--) {
            push @gpcr_subfamily, $select->fetchrow_array();
        }
   @gpcr_subfamily;
} # sub GetGpcrSubForGproteinSub {

sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{id} = 0;
    $this->{gpcr_fam} = 0;
    $this->{gpcr_sub} = '';
    $this->{coupling} = '';
    $this->{pubmed} = 0;

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
		$this->{gpcr_fam} = shift @attr;
		$this->{gpcr_sub} = shift @attr;
		$this->{coupling} = shift @attr;
		$this->{pubmed} = shift @attr;
	} else {
	    carp "Initializing gprotein_gpcr : unexpected number of records = ",$select->rows,"\n";
	}
    }
}


1;
