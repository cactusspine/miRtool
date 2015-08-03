package DbSearchLookup;

##########################################
##
## Document   : DbSearchLookup.pm
## Created on : June 30th, 2009
## Author     : Venkata P. Satagopam (venkata.satagopam@embl.de)
##
##########################################

use DbSessionGpdb;
use Carp;

use base DeepPrintable;

use constant ID_LOAD_STATEMENT => "SELECT * FROM search_lookup WHERE id=?";

sub auto_detect {
        my $str = shift;
#       my $temp_file = "/tmp/temp/bs.txt";
#       close(TEMP_FILE);
#       open(TEMP_FILE, ">$temp_file");
#       print TEMP_FILE "str : $str\n";
#       close(TEMP_FILE);
        my @names = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT DISTINCT term FROM search_lookup WHERE term LIKE '$str%' ORDER BY term LIMIT 20");
        $select->execute();
        my $nr = $select->rows();
        while ($nr--) {
                push @names, $select->fetchrow_array();
        }
        @names;
}

sub GetIdsForTerm {
	my $term = shift; 
	my $gpcr_ids = ();
	my $gprotein_ids = ();
	my $effector_ids = ();
	my $databaseHandle = DbSessionGpdb::GetConnection();
# gpcr
#	my $select = $databaseHandle->prepare("SELECT DISTINCT dbid FROM search_lookup WHERE term=? AND category=\"gpcr\"");
	my $select = $databaseHandle->prepare("SELECT DISTINCT dbid FROM search_lookup WHERE term LIKE '$term%' AND category=\"gpcr\"");
	$select->execute();
        my $nr = $select->rows();
        while ($nr--) {
                push @gpcr_ids, $select->fetchrow_array();
        }

# gprotein
#	$select = $databaseHandle->prepare("SELECT DISTINCT dbid FROM search_lookup WHERE term=? AND category=\"gprotein\"");
	$select = $databaseHandle->prepare("SELECT DISTINCT dbid FROM search_lookup WHERE term LIKE '$term%' AND category=\"gprotein\"");
        $select->execute();
        $nr = $select->rows();
        while ($nr--) {
                push @gprotein_ids, $select->fetchrow_array();
        }

# effectors
#        $select = $databaseHandle->prepare("SELECT DISTINCT dbid FROM search_lookup WHERE term=? AND category=\"effector\"");
        $select = $databaseHandle->prepare("SELECT DISTINCT dbid FROM search_lookup WHERE term LIKE '$term%' AND category=\"effector\"");
        $select->execute();
        $nr = $select->rows();
        while ($nr--) {
                push @effector_ids, $select->fetchrow_array();
        }

	my %result = (gpcr_ids=>\@gpcr_ids, gprotein_ids=>\@gprotein_ids, effector_ids=>\@effector_ids);
	\%result;
} # sub GetIdsForTerm {
 

sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{DBID} = 0;
    $this->{term} = '';
    $this->{dbid} = '';
    $this->{category} = '';

    $this->_initialize(@_);
    $this;
}

sub _initialize {
    my $this = shift;
    my $criteria = shift;
    my $loadStatement = '';
#    if ($criteria=~/^\d+$/) {
        $loadStatement = ID_LOAD_STATEMENT;
#    } else {
#        $loadStatement = GENE_LOAD_STATEMENT;
#    }
    if ($criteria) {
	my $databaseHandle = DbSessionGpdb::GetConnection();
	my $select = $databaseHandle->prepare($loadStatement);
	$select->execute($criteria);
	if ($select->rows == 1) {
	    my @attr = $select->fetchrow_array;
	    $this->{DBID} = shift @attr;
            $this->{term} = shift @attr;
            $this->{dbid} = shift @attr;
            $this->{category} = shift @attr;
	} else {
	    carp "Initializing eff_validation : unexpected number of records = ",$select->rows,"\n";
	}
    }
}

1;
