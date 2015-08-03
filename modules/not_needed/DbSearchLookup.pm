package DbSearchLookup;

##########################################
##
## Document   : DbSearchLookup.pm
## Created on : Jan 18th, 2010
## Author     : Venkata P. Satagopam (venkata.satagopam@embl.de)
##
##########################################

use DbSession;
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
        my $databaseHandle = DbSession::GetConnection();
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
	my $human_ids = ();
	my $mouse_ids = ();
	my $yeast_ids = ();
	my $databaseHandle = DbSession::GetConnection();
# human
#	my $select = $databaseHandle->prepare("SELECT DISTINCT dbid FROM search_lookup WHERE term=? AND org=\"human\"");
	my $select = $databaseHandle->prepare("SELECT DISTINCT dbid FROM search_lookup WHERE term LIKE '$term%' AND org=\"human\"");
	$select->execute();
        my $nr = $select->rows();
        while ($nr--) {
                push @human_ids, $select->fetchrow_array();
        }

# mouse
#	$select = $databaseHandle->prepare("SELECT DISTINCT dbid FROM search_lookup WHERE term=? AND org=\"mouse\"");
	$select = $databaseHandle->prepare("SELECT DISTINCT dbid FROM search_lookup WHERE term LIKE '$term%' AND org=\"mouse\"");
        $select->execute();
        $nr = $select->rows();
        while ($nr--) {
                push @mouse_ids, $select->fetchrow_array();
        }

# yeasts
#        $select = $databaseHandle->prepare("SELECT DISTINCT dbid FROM search_lookup WHERE term=? AND org=\"yeast\"");
        $select = $databaseHandle->prepare("SELECT DISTINCT dbid FROM search_lookup WHERE term LIKE '$term%' AND org=\"yeast\"");
        $select->execute();
        $nr = $select->rows();
        while ($nr--) {
                push @yeast_ids, $select->fetchrow_array();
        }

	my %result = (human_ids=>\@human_ids, mouse_ids=>\@mouse_ids, yeast_ids=>\@yeast_ids);
	\%result;
} # sub GetIdsForTerm {
 

sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{DBID} = 0;
    $this->{term} = '';
    $this->{dbid} = '';
    $this->{org} = '';

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
	my $databaseHandle = DbSession::GetConnection();
	my $select = $databaseHandle->prepare($loadStatement);
	$select->execute($criteria);
	if ($select->rows == 1) {
	    my @attr = $select->fetchrow_array;
	    			$this->{DBID} = shift @attr;
            $this->{term} = shift @attr;
            $this->{dbid} = shift @attr;
            $this->{org} = shift @attr;
	} else {
	    carp "Initializing eff_validation : unexpected number of records = ",$select->rows,"\n";
	}
    }
}

1;
