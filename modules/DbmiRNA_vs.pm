package DbmiRNA;;

use DbSession;
use Carp;

use base DeepPrintable;

use constant ID_LOAD_STATEMENT => "SELECT * FROM mirna WHERE id=?";

use constant GENE_LOAD_STATEMENT => "SELECT * FROM mirna WHERE mirna_name=?";

sub GetTableViewInfo {
	my ($field_name, $asse_or_desc, $tmp_database, $tmp_table) = @_;
  my %target_hash = ();
	my %mirna_hash = ();
	my %result_hash = ();
	
	my %mirna_size_hash = ();
	my %gene_size_hash = ();
	my %transcript_size_hash = ();

	my $statement = "";
	if ($field_name eq "mirbase_name") {
		$statement = "SELECT m.* FROM systec.mirna m, $tmp_database.$tmp_table t WHERE t.gene = m.mirna_name ORDER BY m.mirna_name $asse_or_desc";
	}
	elsif ($field_name eq "mirbase_id") {
		$statement = "SELECT m.* FROM systec.mirna m, $tmp_database.$tmp_table t WHERE t.gene = m.mirna_acc ORDER BY m.mirna_acc $asse_or_desc";
	}

  my $dbh = DbSession::GetConnection();
	if (! $dbh) {
		die "There is no connection to the database." . $DBI::errstr;
	}
  my $select = $dbh->prepare($statement) or die "Unable to prepare $statement" . $dbh->errstr();
  $select->execute() or die "Unable to execute $statement.  " . $select->errstr();
  my $nr = $select->rows();
	my @data;
	my $i = 0;
  while ($nr--) {
		$i++;
		@data = $select->fetchrow_array();
    $id 			        = $data[0];
    $mirna_name       = $data[1];
#print "mirna_name : $mirna_name\n";
    $mirna_acc        = $data[2];
    $mirna_chr        = $data[3];
    $mirna_start      = $data[4];
    $mirna_stop       = $data[5];
    $mirna_strand     = $data[6];
    $mirna_mirbase    = $data[7];
    $mirna_targetscan = $data[8];
    $mirna_pictar     = $data[9];
    $mirna_starbase   = $data[10];
    $mirna_mirdb      = $data[11];
    $mirna_score      = $data[12];
    $transcript_id    = $data[13];
    $transcript_start = $data[14];
    $transcript_stop  = $data[15];
    $transcript_name  = $data[16];
    $transcript_status    = $data[17];
    $transcript_microcosm = $data[18];
    $transcript_targetscan= $data[19];
    $transcript_pictar    = $data[20];
    $transcript_starbase  = $data[21];
    $transcript_mirdb     = $data[22];
    $transcript_score     = $data[23];
    $gene_id              = $data[24];
    $gene_chr             = $data[25];
    $gene_start           = $data[26];
    $gene_stop            = $data[27];
    $gene_strand          = $data[28];
    $gene_name            = $data[29];
    $description          = $data[30];
    $gene_biotype         = $data[31];
    $gene_status          = $data[32];
    $transcript_count     = $data[33];
$mirna_hash{$mirna_name}{'mirna_acc'}=$mirna_acc;
$mirna_hash{$mirna_name}{'mirna_chr'}=$mirna_chr;
$mirna_hash{$mirna_name}{'mirna_start'}=$mirna_start;
$mirna_hash{$mirna_name}{'mirna_stop'}=$mirna_stop;
$mirna_hash{$mirna_name}{'mirna_strand'}=$mirna_strand;
$mirna_hash{$mirna_name}{'mirna_mirbase'}=$mirna_mirbase;
$mirna_hash{$mirna_name}{'mirna_targetscan'}=$mirna_targetscan;
$mirna_hash{$mirna_name}{'mirna_pictar'}=$mirna_pictar;
$mirna_hash{$mirna_name}{'mirna_starbase'}=$mirna_starbase;
$mirna_hash{$mirna_name}{'mirna_mirdb'}=$mirna_mirdb;
$mirna_hash{$mirna_name}{'mirna_score'}=$mirna_score;

$target_hash{$mirna_name}{$transcript_id}{'transcript_id'} =$transcript_id;
$target_hash{$mirna_name}{$transcript_id}{'transcript_start'} =$transcript_start;
$target_hash{$mirna_name}{$transcript_id}{'transcript_stop'} =$transcript_stop;
$target_hash{$mirna_name}{$transcript_id}{'transcript_name'} =$transcript_name;
$target_hash{$mirna_name}{$transcript_id}{'transcript_status'} =$transcript_status;
$target_hash{$mirna_name}{$transcript_id}{'transcript_microcosm'} =$transcript_microcosm;
$target_hash{$mirna_name}{$transcript_id}{'transcript_targetscan'} =$transcript_targetscan;
$target_hash{$mirna_name}{$transcript_id}{'transcript_pictar'} =$transcript_pictar;
$target_hash{$mirna_name}{$transcript_id}{'transcript_starbase'} =$transcript_starbase;
$target_hash{$mirna_name}{$transcript_id}{'transcript_mirdb'} =$transcript_mirdb;
$target_hash{$mirna_name}{$transcript_id}{'transcript_score'} =$transcript_score;
$target_hash{$mirna_name}{$transcript_id}{'gene_id'} =$gene_id;
$target_hash{$mirna_name}{$transcript_id}{'gene_chr'} =$gene_chr;
$target_hash{$mirna_name}{$transcript_id}{'gene_start'} =$gene_start;
$target_hash{$mirna_name}{$transcript_id}{'gene_stop'} =$gene_stop;
$target_hash{$mirna_name}{$transcript_id}{'gene_strand'} =$gene_strand;
$target_hash{$mirna_name}{$transcript_id}{'gene_name'} =$gene_name;
$target_hash{$mirna_name}{$transcript_id}{'description'} =$description;
$target_hash{$mirna_name}{$transcript_id}{'gene_biotype'} =$gene_biotype;
$target_hash{$mirna_name}{$transcript_id}{'gene_status'} =$gene_status;
$target_hash{$mirna_name}{$transcript_id}{'transcript_count'} =$transcript_count;

	$mirna_size_hash{$mirna_name} = 1;
	$gene_size_hash{$gene_id} = 1;
	$transcript_size_hash{$transcript_id} = 1;
        }

	%result_hash=(mirna_hash=>\%mirna_hash, target_hash=>\%target_hash, mirna_size_hash=>\%mirna_size_hash, gene_size_hash=>\%gene_size_hash, transcript_size_hash=>\%transcript_size_hash);
 return	\%result_hash;
} # sub GetTableViewInfo {

sub GetGeneCentricTableViewInfo {
	my ($field_name, $asse_or_desc, $tmp_database, $tmp_table) = @_;
  my %target_hash = ();
	my %mirna_hash = ();
	my %result_hash = ();

	my %mirna_size_hash = ();
	my %gene_size_hash = ();
	my %transcript_size_hash = ();

	my $statement = "";
### here ids always will be ensembl
	$statement = "SELECT m.* FROM systec.mirna m, $tmp_database.$tmp_table t WHERE t.gene = m.gene_id ORDER BY m.mirna_name $asse_or_desc";

        my $dbh = DbSession::GetConnection();
	if (! $dbh) {
		die "There is no connection to the database." . $DBI::errstr;
	}
        my $select = $dbh->prepare($statement) or die "Unable to prepare $statement" . $dbh->errstr();
        $select->execute() or die "Unable to execute $statement.  " . $select->errstr();
        my $nr = $select->rows();
	my @data;
	my $i = 0;
        while ($nr--) {
		$i++;
		@data = $select->fetchrow_array();
    $id 			        = $data[0];
    $mirna_name       = $data[1];
#print "mirna_name : $mirna_name\n";
    $mirna_acc        = $data[2];
    $mirna_chr        = $data[3];
    $mirna_start      = $data[4];
    $mirna_stop       = $data[5];
    $mirna_strand     = $data[6];
    $mirna_mirbase    = $data[7];
    $mirna_targetscan = $data[8];
    $mirna_pictar     = $data[9];
    $mirna_starbase   = $data[10];
    $mirna_mirdb      = $data[11];
    $mirna_score      = $data[12];
    $transcript_id    = $data[13];
    $transcript_start = $data[14];
    $transcript_stop  = $data[15];
    $transcript_name  = $data[16];
    $transcript_status    = $data[17];
    $transcript_microcosm = $data[18];
    $transcript_targetscan= $data[19];
    $transcript_pictar    = $data[20];
    $transcript_starbase  = $data[21];
    $transcript_mirdb     = $data[22];
    $transcript_score     = $data[23];
    $gene_id              = $data[24];
    $gene_chr             = $data[25];
    $gene_start           = $data[26];
    $gene_stop            = $data[27];
    $gene_strand          = $data[28];
    $gene_name            = $data[29];
    $description          = $data[30];
    $gene_biotype         = $data[31];
    $gene_status          = $data[32];
    $transcript_count     = $data[33];



$mirna_hash{$transcript_id}{$mirna_name}{'mirna_acc'}=$mirna_acc;
$mirna_hash{$transcript_id}{$mirna_name}{'mirna_chr'}=$mirna_chr;
$mirna_hash{$transcript_id}{$mirna_name}{'mirna_start'}=$mirna_start;
$mirna_hash{$transcript_id}{$mirna_name}{'mirna_stop'}=$mirna_stop;
$mirna_hash{$transcript_id}{$mirna_name}{'mirna_strand'}=$mirna_strand;
$mirna_hash{$transcript_id}{$mirna_name}{'mirna_mirbase'}=$mirna_mirbase;
$mirna_hash{$transcript_id}{$mirna_name}{'mirna_targetscan'}=$mirna_targetscan;
$mirna_hash{$transcript_id}{$mirna_name}{'mirna_pictar'}=$mirna_pictar;
$mirna_hash{$transcript_id}{$mirna_name}{'mirna_starbase'}=$mirna_starbase;
$mirna_hash{$transcript_id}{$mirna_name}{'mirna_mirdb'}=$mirna_mirdb;
$mirna_hash{$transcript_id}{$mirna_name}{'mirna_score'}=$mirna_score;

$target_hash{$transcript_id}{'transcript_start'} =$transcript_start;
$target_hash{$transcript_id}{'transcript_stop'} =$transcript_stop;
$target_hash{$transcript_id}{'transcript_name'} =$transcript_name;
$target_hash{$transcript_id}{'transcript_status'} =$transcript_status;
$target_hash{$transcript_id}{'transcript_microcosm'} =$transcript_microcosm;
$target_hash{$transcript_id}{'transcript_targetscan'} =$transcript_targetscan;
$target_hash{$transcript_id}{'transcript_pictar'} =$transcript_pictar;
$target_hash{$transcript_id}{'transcript_starbase'} =$transcript_starbase;
$target_hash{$transcript_id}{'transcript_mirdb'} =$transcript_mirdb;
$target_hash{$transcript_id}{'transcript_score'} =$transcript_score;
$target_hash{$transcript_id}{'gene_id'} =$gene_id;
$target_hash{$transcript_id}{'gene_chr'} =$gene_chr;
$target_hash{$transcript_id}{'gene_start'} =$gene_start;
$target_hash{$transcript_id}{'gene_stop'} =$gene_stop;
$target_hash{$transcript_id}{'gene_strand'} =$gene_strand;
$target_hash{$transcript_id}{'gene_name'} =$gene_name;
$target_hash{$transcript_id}{'description'} =$description;
$target_hash{$transcript_id}{'gene_biotype'} =$gene_biotype;
$target_hash{$transcript_id}{'gene_status'} =$gene_status;
$target_hash{$transcript_id}{'transcript_count'} =$transcript_count;

	$mirna_size_hash{$mirna_name} = 1;
	$gene_size_hash{$gene_id} = 1;
	$transcript_size_hash{$transcript_id} = 1;
        }

#	%result_hash=(mirna_hash=>\%mirna_hash, target_hash=>\%target_hash);
	%result_hash=(mirna_hash=>\%mirna_hash, target_hash=>\%target_hash, mirna_size_hash=>\%mirna_size_hash, gene_size_hash=>\%gene_size_hash, transcript_size_hash=>\%transcript_size_hash);
 return	\%result_hash;
} # sub GeneCentricGetTableViewInfo {

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

    if ($criteria =~ /^\d+$/) {
        $loadStatement = ID_LOAD_STATEMENT;
    } else {
        $loadStatement = GENE_LOAD_STATEMENT;
    }

    if ($criteria) {
	my $dbh = DbSession::GetConnection();
	if (! $dbh) {
		die "There is no connection to the database." . $DBI::errstr;
	}

	my $select = $dbh->prepare($loadStatement) or die "Unable to prepare $loadStatement" . $dbh->errstr();
	$select->execute($criteria) or die "Unable to execute $loadStatement.  " . $select->errstr();
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
