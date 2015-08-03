package DbPseudogeneGeneFeatures;

use DbSession;
use Carp;

use base DeepPrintable;

use constant ID_LOAD_STATEMENT => "SELECT * FROM pseudogene_geneFeatures WHERE id=?";


sub new {
    my $class = shift;
    my $this = $class->SUPER::new();

    $this->{DBID} = 0;
    $this->{mirna_name}  ='';
    $this->{mirna_acc}  ='';
    $this->{mirna_chr} = '';
    $this->{mirna_start} =0;
    $this->{mirna_stop}  =0;
    $this->{mirna_strand} = '';
    $this->{mirna_mirbase} = '';
    $this->{mirna_targetscan} ='';
    $this->{mirna_pictar} ='';
    $this->{mirna_starbase} ='';
    $this->{mirna_mirdb} ='';
    $this->{mirna_score} ='';
    $this->{transcript_id} ='';
    $this->{transcript_start} =0;
    $this->{transcript_stop} =0;
    $this->{transcript_name} ='';
    $this->{transcript_status} ='';
    $this->{transcript_microcosm} ='';
    $this->{transcript_targetscan} ='';
    $this->{transcript_pictar} ='';
    $this->{transcript_starbase} ='';
    $this->{transcript_mirdb} ='';
    $this->{transcript_score} ='';
    $this->{gene_id} ='';
    $this->{gene_chr} ='';
    $this->{gene_start} =0;
    $this->{gene_stop} =0;
    $this->{gene_strand} ='';
    $this->{gene_name} ='';
    $this->{description} ='';
    $this->{gene_biotype} ='';
    $this->{gene_status} ='';
    $this->{transcript_count} =0;

    $this->_initialize(@_);
    $this;
}

sub _initialize {
    my $this = shift;
    my $criteria = shift;
    my $load = '';
    my $loadStatement = ID_LOAD_STATEMENT;

    if ($criteria) {
	my $databaseHandle = DbSession::GetConnection();
	my $select = $databaseHandle->prepare($loadStatement);
	$select->execute($criteria);
	if ($select->rows == 1) {
		my @attr = $select->fetchrow_array;
    $this->{DBID} 			      = shift @attr;
    $this->{mirna_name}       = shift @attr;
    $this->{mirna_acc}        = shift @attr;
    $this->{mirna_chr}        = shift @attr;
    $this->{mirna_start}      = shift @attr;
    $this->{mirna_stop}       = shift @attr;
    $this->{mirna_strand}     = shift @attr;
    $this->{mirna_mirbase}    = shift @attr;
    $this->{mirna_targetscan} = shift @attr;
    $this->{mirna_pictar}     = shift @attr;
    $this->{mirna_starbase}   = shift @attr;
    $this->{mirna_mirdb}      = shift @attr;
    $this->{mirna_score}      = shift @attr;
    $this->{transcript_id}    = shift @attr;
    $this->{transcript_start} = shift @attr;
    $this->{transcript_stop}  = shift @attr;
    $this->{transcript_name}  = shift @attr;
    $this->{transcript_status}    = shift @attr;
    $this->{transcript_microcosm} = shift @attr;
    $this->{transcript_targetscan}= shift @attr;
    $this->{transcript_pictar}    = shift @attr;
    $this->{transcript_starbase}  = shift @attr;
    $this->{transcript_mirdb}     = shift @attr;
    $this->{transcript_score}     = shift @attr;
    $this->{gene_id}              = shift @attr;
    $this->{gene_chr}             = shift @attr;
    $this->{gene_start}           = shift @attr;
    $this->{gene_stop}            = shift @attr;
    $this->{gene_strand}          = shift @attr;
    $this->{gene_name}            = shift @attr;
    $this->{description}          = shift @attr;
    $this->{gene_biotype}         = shift @attr;
    $this->{gene_status}          = shift @attr;
    $this->{transcript_count}     = shift @attr;
	} else {
	    carp "Initializing human_summary_sheet : unexpected number of records = ",$select->rows,"\n";
	}
    }
}


1;
