package DbGproteinEffector;

##########################################
##
## Document   : DbGproteinEffector.pm
## Created on : June 25th, 2009
## Author     : Venkata P. Satagopam (venkata.satagopam@embl.de)
##
##########################################

use DbSessionGpdb;
use Carp;

use base DeepPrintable;

use constant LOAD_STATEMENT => "SELECT * FROM gprotein_effector WHERE id=?";


sub GetEffectorIdsForGproteinId {
	my $gprotein_id = shift;
	my @effector_ids = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT DISTINCT(e.id)  FROM gprotein_effector ge, effector e, gprotein g WHERE g.id=? AND ge.effector=e.type AND ge.subfamily=g.subfamily");
        $select->execute($gprotein_id);
	my $nr = $select->rows();
       while ($nr--) {
           push @effector_ids, $select->fetchrow_array();
        }
   @effector_ids;	
} # sub GetEffectorIdsForGproteinId {

sub GetEffectorDetailsForGproteinId {
        my $gprotein_id = shift;
        my %effector_details_hash = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT DISTINCT(e.id), e.name, ge.regulation, ge.pubmed  FROM gprotein_effector ge, effector e, gprotein g WHERE g.id=? AND ge.effector=e.type AND ge.subfamily=g.subfamily");
        $select->execute($gprotein_id);
        my $nr = $select->rows();
	my @data;
       	while ($nr--) {
		@data = $select->fetchrow_array();
		my $id = $data[0];
                my $name = $data[1];
                my $regulation = $data[2];
                my $pubmed = $data[3];
		$effector_details_hash{$id}{name} = $name;
		$effector_details_hash{$id}{regulation} = $regulation;
		$effector_details_hash{$id}{pubmed} = $pubmed;
        }
   \%effector_details_hash;
} # sub GetEffectorDetailsForGproteinId {

sub GetGproteinIdsForEffectorId {
        my $effector_id = shift;
        my @gprotein_ids = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT DISTINCT(g.id)  FROM gprotein_effector ge, effector e, gprotein g WHERE e.id=? AND ge.effector=e.type AND ge.subfamily=g.subfamily");
        $select->execute($effector_id);
        my $nr = $select->rows();
       while ($nr--) {
           push @gprotein_ids, $select->fetchrow_array();
        }
   @gprotein_ids;
} # sub GetGproteinIdsForEffectorId {

sub GetGproteinDetailsForEffectorId {
        my $effector_id = shift;
        my %gprotein_details_hash = (); 
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT DISTINCT(g.id),g.name, ge.regulation, ge.pubmed  FROM gprotein_effector ge, effector e, gprotein g WHERE e.id=? AND ge.effector=e.type AND ge.subfamily=g.subfamily");
        $select->execute($effector_id);
        my $nr = $select->rows();
	my @data;
       	while ($nr--) {
		@data = $select->fetchrow_array();
		my $id = $data[0];
                my $name = $data[1];
                my $regulation = $data[2];
                my $pubmed = $data[3];
		$gprotein_details_hash{$id}{name} = $name;
		$gprotein_details_hash{$id}{regulation} = $regulation;
		$gprotein_details_hash{$id}{pubmed} = $pubmed;
        }
   \%gprotein_details_hash;
} # sub GetGproteinDetailsForEffectorId {


sub GetEffectorSubForGproteinSub {
        my $gprotein_subfamily = shift;
        my @effector_sub = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT DISTINCT(e.subfamily)  FROM gprotein_effector ge, effector e WHERE ge.subfamily=? AND ge.effector = e.type");
        $select->execute($gprotein_subfamily);
        my $nr = $select->rows();
       while ($nr--) {
           push @effector_sub, $select->fetchrow_array();
        }
   @effector_sub;
} # sub GetEffectorSubForGproteinSub {

sub GetGproteinSubForEffectorSub {
        my $effector_sub = shift;
        my @gprotein_subfamily = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT DISTINCT(ge.subfamily)  FROM gprotein_effector ge, effector e WHERE e.subfamily=? AND ge.effector = e.type");
        $select->execute($effector_sub);
        my $nr = $select->rows();
       while ($nr--) {
           push @gprotein_subfamily, $select->fetchrow_array();
        }
   @gprotein_subfamily;
} # sub GetGproteinSubForEffectorSub {

sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{id} = 0;
    $this->{subfamily} = '';
    $this->{effector} =''; 
    $this->{regulation} = '';
    $this->{pubmed} = '';

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
		$this->{subfamily} = shift @attr;
		$this->{effector} = shift @attr;
		$this->{regulation} = shift @attr;
		$this->{pubmed} = shift @attr;
	} else {
	    carp "Initializing gprotein_effector : unexpected number of records = ",$select->rows,"\n";
	}
    }
}


1;
