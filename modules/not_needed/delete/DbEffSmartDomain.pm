package DbEffSmartDomain;

##########################################
##
## Document   : DbEffSmartDomain.pm
## Created on : May 27th, 2009
## Author     : Venkata P. Satagopam (venkata.satagopam@embl.de)
##
##########################################

use DbSessionGpdb;
use Carp;

use base DeepPrintable;


use constant ID_LOAD_STATEMENT => "SELECT * FROM eff_smart_domains WHERE id=?";
#use constant PROTEIN_LOAD_STATEMENT => "SELECT * FROM eff_smart_domains WHERE protein=?";


sub GetProteinIdsForDomain {
	my $domain = shift;
        my @proteinIds = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $statement = "SELECT DISTINCT(protein_id) FROM eff_smart_domains WHERE description=?";
        my $select = $databaseHandle->prepare($statement);
        $select->execute($domain);
        my $nr = $select->rows();
        while ($nr--) {
                push @proteinIds, $select->fetchrow_array();
        } # while ($nr--) {
        @proteinIds;
} # sub GetProteinIdsForDomain {

sub GetAllProteinIds {
        my @proteinIds = ();
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $statement = "SELECT DISTINCT(protein_id) FROM eff_smart_domains";
        my $select = $databaseHandle->prepare($statement);
        $select->execute();
        my $nr = $select->rows();
        while ($nr--) {
                push @proteinIds, $select->fetchrow_array();
        } # while ($nr--) {
        @proteinIds;
} # sub GetAllProteinIds {


sub GetDomainIdsForPIDandDBName {
	my ($protein_id) = shift;
	my @domainsIds = ();
	if ($protein_id) {
		my $databaseHandle = DbSessionGpdb::GetConnection();
		my $statement = "";
		$statement = "SELECT id FROM eff_smart_domains WHERE protein_id=? ORDER BY start";
		my $select = $databaseHandle->prepare($statement);
		$select->execute($protein_id);
		my $nr = $select->rows();
	        while ($nr--) {
			push @domainsIds, $select->fetchrow_array();
		} # while ($nr--) {
	} # if ($protein_id) {
	@domainsIds;
} # sub GetDomainIdsForPIDandDBName {

sub GetDomainIdsForProtein {
        my ($protein) = shift;
        my @domainsIds = ();
        if ($protein) {
                my $databaseHandle = DbSessionGpdb::GetConnection();
                my $statement = "";
                $statement = "SELECT id FROM eff_smart_domains WHERE protein=? ORDER BY start";
                my $select = $databaseHandle->prepare($statement);
                $select->execute($protein);
                my $nr = $select->rows();
                while ($nr--) {
                        push @domainsIds, $select->fetchrow_array();
                } # while ($nr--) {
        } # if ($protein) {
        @domainsIds;
} # sub GetDomainIdsForProtein {

sub getSmartDomainInfoForProtein {
        my ($protein) = @_;
        my @domainsIds = ();
        @domainsIds = &DbProgeriaSmartDomain::GetDomainIdsForProtein($protein);
        my @domains = ();
        foreach my $d (@domainsIds) {
                my $domain;
                $domain = new DbProgeriaSmartDomain($d);
                if ($domain->{Description}) {
                        push @domains, $domain;
                }
        } # foreach my $d (@clusterDomainsIds) {
        return \@domains
} # sub getSmartDomainInfoForProtein {



sub GetProteinIdsForProteins{
        my $proteins = shift;
        my @proteins = @$proteins;
#print "proteins : @proteins\n";
        my @ids = ();
	my $databaseHandle = DbSessionGpdb::GetConnection();
        my $statement = "";

        foreach my $p (@proteins) {
                $statement = "SELECT DISTINCT(protein_id) FROM eff_smart_domains WHERE protein=?";
		my $select = $databaseHandle->prepare($statement);
                $select->execute($p);
                push @ids, $select->fetchrow_array();
        }
        @ids;
} # sub GetProteinIdsForProteins {

sub GetProteinForProteinId {
        my $protein_id = shift;
        my $protein = "";
        my $databaseHandle = DbSessionGpdb::GetConnection();
        my $statement = "";

        $statement = "SELECT DISTINCT(protein) FROM eff_smart_domains WHERE protein_id=?";
        my $select = $databaseHandle->prepare($statement);
        $select->execute($protein_id);
        $protein = $select->fetchrow_array();
        $protein;
} # sub GetProteinForProteinId {


sub GetSmartProteinIdsDomainMaxMin {
        my (@protein_ids) = @_;
        my @min_max = ();
	my $databaseHandle = DbSessionGpdb::GetConnection();
        my $select = "";
        foreach my $p (@protein_ids) {
                $select = $databaseHandle->prepare("SELECT min(start), max(end) FROM eff_smart_domains  WHERE protein_id=?");
                $select->execute($p);
                push @min_max, $select->fetchrow_array();
        } # foreach my @protein_ids {
        @min_max;
} # sub GetSmartProteinsDomainMaxMin {


sub getSmartDomainInfo {
        my ($protein_id) = @_;
        my @clusterDomainsIds = ();
        @clusterDomainsIds = &GetDomainIdsForPIDandDBName($protein_id);
        my @domains = ();
        foreach my $d (@clusterDomainsIds) {
                my $domain;
                $domain = new DbEffSmartDomain($d);
                if ($domain->{Description}) {
                        push @domains, $domain;
                }
        } # foreach my $d (@clusterDomainsIds) {
        return \@domains
} # sub getSmartDomainInfo {

sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{DBID} = 0;
    $this->{ProteinID} = '';
    $this->{Protein} = '';
    $this->{DBName} = '';
    $this->{Description} = '';
    $this->{Start} = 0;
    $this->{End} = 0;

    $this->_initialize(@_);
    $this;
}

sub _initialize {
    my $this = shift;
    my $criteria = shift;
    my $loadStatement = '';
#    if ($criteria =~ /^\d+$/) {
        $loadStatement = ID_LOAD_STATEMENT;
#    } else {
#        $loadStatement = PROTEIN_LOAD_STATEMENT;
#    }

    if ($criteria) {
	my $databaseHandle = DbSessionGpdb::GetConnection();
	my $select = $databaseHandle->prepare($loadStatement);
	$select->execute($criteria);
	if ($select->rows == 1) {
	    my @attr = $select->fetchrow_array;
	    $this->{DBID} = shift @attr;
            $this->{ProteinID} = shift @attr;	
            $this->{Protein} = shift @attr;
            $this->{DBName} = shift @attr;
            $this->{Description} = shift @attr;
            $this->{Start} = shift @attr;
            $this->{End} = shift @attr;
	} else {
	    carp "Initializing TAMAHUD SMART DOMAINS : unexpected number of records = ",$select->rows,"\n";
	}
    }
}


1;
