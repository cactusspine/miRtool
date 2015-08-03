package DbGpcrValidation;

##########################################
##
## Document   : DbGpcrValidation.pm
## Created on : June 5th, 2009
## Author     : Venkata P. Satagopam (venkata.satagopam@embl.de)
##
##########################################

use DbSessionGpdb;
use Carp;

use base DeepPrintable;

use constant GENE_SELECT_STATEMENT => "SELECT id FROM gpcr_validation WHERE ensembl_gene=?";
#use constant GENE_LOAD_STATEMENT => "SELECT * FROM gpcr_validation WHERE sp_pir_id=?";
use constant ID_LOAD_STATEMENT => "SELECT * FROM gpcr_validation WHERE id=?";

#sub GetGpcrValidationIdForHugoName {
#    my $hugo_name = shift;
#    
#    my $gpcr_validation_id = "";
#    if ($hugo_name) {
#	my $databaseHandle = DbSessionGpdb::GetConnection();
#	my $select = $databaseHandle->prepare(HUGO_SELECT_STATEMENT);
#	$select->execute($hugo_name);
#	$gpcr_validation_id = $select->fetchrow_array();
#    }
#    $gpcr_validation_id;
#}

sub GetEnsemblGeneForUniprotId {
    my $sp_pir_id = shift;

    my @ensg = ();
    if ($sp_pir_id) {
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare("SELECT ensembl_gene FROM gpcr_validation WHERE sp_pir_id=?");
        $select->execute($sp_pir_id);
        push @ensg, $select->fetchrow_array();
    }
    $ensg[0];
} # sub GetEnsemblGeneForUniprotId {

sub GetGpcrValidationIdForGene {
    my $gene = shift;

    my $gpcr_validation_id = "";
    if ($gene) {
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = $databaseHandle->prepare(GENE_SELECT_STATEMENT);
        $select->execute($gene);
        $gpcr_validation_id = $select->fetchrow_array();
    }
    $gpcr_validation_id;
}

sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{DBID} = 0;
    $this->{sp_pir_id} = '';
    $this->{sp_acc} = '';
    $this->{ensembl_gene} = '';

    $this->_initialize(@_);
    $this;
}

sub _initialize {
    my $this = shift;
    my $criteria = shift;
    my $loadStatement = '';
    if ($criteria=~/^\d+$/) {
        $loadStatement = ID_LOAD_STATEMENT;
    } 
#    else {
#        $loadStatement = GENE_LOAD_STATEMENT;
#    }
    if ($criteria) {
	my $databaseHandle = DbSessionGpdb::GetConnection();
	my $select = $databaseHandle->prepare($loadStatement);
	$select->execute($criteria);
	if ($select->rows == 1) {
	    my @attr = $select->fetchrow_array;
	    $this->{DBID} = shift @attr;
            $this->{sp_pir_id} = shift @attr;
            $this->{sp_acc} = shift @attr;
            $this->{ensembl_gene} = shift @attr;
	} else {
	    carp "Initializing gpcr_validation : unexpected number of records = ",$select->rows,"\n";
	}
    }
}

1;
