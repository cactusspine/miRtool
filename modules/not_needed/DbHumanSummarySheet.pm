package DbHumanSummarySheet;

use DbSession;
use Carp;

use base DeepPrintable;

use constant ID_LOAD_STATEMENT => "SELECT * FROM human_summary_sheet WHERE id=?";

use constant GENE_LOAD_STATEMENT => "SELECT * FROM human_summary_sheet WHERE gene=?";

sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{DBID} = 0;
    $this->{Gene}  ='';
    $this->{Transcript}  ='';
    $this->{Protein} = '';
    $this->{Description} ='';
    $this->{ChromosomeName}  ='';
    $this->{GeneStart} = 0;
    $this->{GeneEnd} = 0;
    $this->{GO} ='';
    $this->{EmblGenbankID} ='';
    $this->{EntrezgeneID} ='';
    $this->{UnigeneID} ='';
    $this->{Interpro} ='';
    $this->{ProteinID} ='';
    $this->{PdbID} ='';
    $this->{PdbFromPdb} ='';
    $this->{PdbFromPssh} ='';
    $this->{HsspID} ='';
    $this->{PsshID} ='';
    $this->{RefseqDNAID} ='';
    $this->{RefseqPeptideID} ='';
    $this->{PfamID} ='';
    $this->{UniprotID} ='';
    $this->{Omim} ='';
    $this->{Panther} ='';
    $this->{Pathway} ='';
    $this->{Reactome} ='';
    $this->{Drugbank} ='';
    $this->{Hmdb} ='';

    $this->_initialize(@_);
    $this;
}

sub _initialize {
    my $this = shift;
    my $criteria = shift;
    my $load = '';

    if ($criteria =~ /^\d+$/) {
        $loadStatement = ID_LOAD_STATEMENT;
    } else {
        $loadStatement = GENE_LOAD_STATEMENT;
    }

    if ($criteria) {
	my $databaseHandle = DbSession::GetConnection();
	my $select = $databaseHandle->prepare($loadStatement);
	$select->execute($criteria);
	if ($select->rows == 1) {
		my @attr = $select->fetchrow_array;
		$this->{DBID} = shift @attr;
		$this->{Gene} = shift @attr;
		$this->{Transcript} = shift @attr;
		$this->{Protein} = shift @attr;
		$this->{Description} = shift @attr;
		$this->{ChromosomeName} = shift @attr;
		$this->{GeneStart} = shift @attr;
		$this->{GeneEnd} = shift @attr;
		$this->{GO} = shift @attr;
		$this->{EmblGenbankID} = shift @attr;
		$this->{EntrezgeneID} = shift @attr;
		$this->{UnigeneID} = shift @attr;
		$this->{Interpro} = shift @attr;
		$this->{ProteinID} = shift @attr;
		$this->{PdbID} = shift @attr;
		$this->{PdbFromPdb} = shift @attr;
		$this->{PdbFromPssh} = shift @attr;
		$this->{HsspID} = shift @attr;
		$this->{PsshID} = shift @attr;
		$this->{RefseqDNAID} = shift @attr;
		$this->{RefseqPeptideID} = shift @attr;
		$this->{PfamID} = shift @attr;
		$this->{UniprotID} = shift @attr;
		$this->{Omim} = shift @attr;
		$this->{Panther} = shift @attr;
		$this->{Pathway} = shift @attr;
		$this->{Reactome} = shift @attr;
		$this->{Drugbank} = shift @attr;
		$this->{Hmdb} = shift @attr;

	} else {
	    carp "Initializing human_summary_sheet : unexpected number of records = ",$select->rows,"\n";
	}
    }
}


1;
