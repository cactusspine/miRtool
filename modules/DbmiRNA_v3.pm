package DbmiRNA;

use DbSession;
use Carp;
#use CGI::Carp;
use base DeepPrintable;
use Storable;
use Data::Dumper qw(Dumper);
my $mir2alias_hash_file="/home/database/projects/gist/systec/mirna/wj/data/miRBase/mir_alias.hash";#this one put the datadir 
my $priority_def =3;#this is temp testing for setting default priority
#this package contain getTableViewInfo, and by the way generate the query result for down loading
#use constant ID_LOAD_STATEMENT => "SELECT * FROM mirna WHERE id=?";

#use constant GENE_LOAD_STATEMENT => "SELECT * FROM mirna WHERE mirna_name=?";
#my $dbh=DbSession::GetConnection();$sth=$dbh->prepare("SELECT m.* FROM gist.mirna_human_strict AS m");my $rv =$sth->execute();$names=$sth->{NAME},print @$names
sub GetMirTableViewInfo {# this is the function 
	my ($field_name, $asse_or_desc,$tmp_database, $tmp_table,$query_database,$tmp_dir,$toolSelection) = @_;#field_name =mirbase _accession or mirbase _name,input type,#add $query_database which indicate the database which it should query ,ie: mirna_human_strict#tmp_dir is the directory of sql files and result files#toolSelection hold hash the tools that has been considered as key 
    my $output_file=$tmp_dir."/query_output.txt";
   
    #print "in side BmiRNA.pm GetMirTableViewInfo \n";
    #print "field name is $field_name \n";
    #print "ORder by $asse_or_desc \n";
    #print "temp data base = $tmp_database \n";
    #print "Table tem is ".$tem_table;
   # print "query DB: $query_database";
    #print ;
    
    close (FH_OUTPUT);#file handle for output file
    open (FH_OUTPUT,">$output_file")||die "Can't open file \n";
    $query_database="gist.".$query_database;
    my $ranked_by="priority";#temperally take priority as ranking
    my %target_hash = ();
	my %mirna_hash = ();#the hash to store mirnaAccession->miRNAAlias
    my %mir2alias_hash=%{retrieve($mir2alias_hash_file)};
	my %result_hash = ();	
	my %priority_hash = ();
	

	my $statement = "";
	if ($field_name=~'mirbase') {
		$statement = "SELECT m.* FROM $query_database m, $tmp_database.$tmp_table t WHERE t.gene = m.mirna_accession AND m.priority >= 3 ORDER BY m.$ranked_by $asse_or_desc";#altered
		#print "Statement is $statement\n";
	}else{ print "there is sth wrong!";}
#	elsif ($field_name eq "refseq_mrna_id") {
#		$statement = "SELECT m.* FROM $query_database m, $tmp_database.$tmp_table t WHERE t.gene = m.refseq_id ORDER BY m.$ranked_by $asse_or_desc";
#	}    
    my $dbh = DbSession::GetConnection();
	if (! $dbh) {
		die "There is no connection to the database." . $DBI::errstr;
	}
    my $select = $dbh->prepare($statement) or die "Unable to prepare $statement" . $dbh->errstr();
    $select->execute() or die "Unable to execute $statement.  " . $select->errstr();
    my $nr = $select->rows();#number of rows found
    #print "number of rows $nr";
	my $fields=$select->{NAME};#get all column names from the database #id#mirbase_accession#refseq_id#differentdbs#last, priority
	my @fields=@$fields;
	
	#print @fields;
    shift @fields;#delete the column of internal id
    print FH_OUTPUT join("\t",@fields),"\n";#put header in the output file
    shift @fields;#delete the column of mirna_id
    shift @fields;#delete the column of refseq_id
    pop @fields;#delete the column of priority
    my ($fields_ref,$index_ref)=&get_included_index(\@fields,$toolSelection);#return the fields name to show accoring to tool selection(array), and index of the data in each row
    @fields=@{$fields_ref}; 
    my %indexes=%{$index_ref};#contains the index of clumn=>weight of each column  
    my @data;#hold the currentline
    my $counter_result=0;
    while(my @data= $select->fetchrow_array){
        #@data= @$row_ref;#get currentline
        my $currentid= shift @data;
        print FH_OUTPUT join ("\t",@data),"\n";
        my $currentmirna= shift @data;
        my $currenttarget=shift @data;
        my $currentpriority=pop @data;
        #$mirna_hash{$currentmirna} = shift @{$mir2alias_hash{$currentmirna}};#the out put of the mirna2_hash is a array take the first one
        #print "$mir2alias_hash{$currentmirna}ref\n";
        #print "@{$mir2alias_hash{$currentmirna}}array<br>";
        #foreach(@{$mir2alias_hash{$currentmirna}}){
        #print $_,"\t";
        #}
        my $currentmirnaname = @{$mir2alias_hash{$currentmirna}}[-1];
        $mirna_hash{$currentmirna} = $currentmirnaname;
        $priority_hash{$currentmirna}{$currenttarget}=0;
        my @output=();
        foreach my $key(keys %indexes){
            push @output, $data[$key];
            if($data[$key] eq "yes"){
            $priority_hash{$currentmirna}{$currenttarget}+=$indexes{$key};}
            
        }
        # $priority_hash{$currenttarget}{$currentmirna}=0+$currentpriority;
        if ($priority_hash{$currentmirna}{$currenttarget}>=$priority_def){
        $target_hash{$currentmirna}{$currenttarget}=\@output;
        $counter_result++;
        }# if ($priority_hash{$currentmirna}{$currenttarget}>=$priority_def){ 
        else{ delete $priority_hash{$currentmirna}{$currenttarget};}
    
    }
    close(FH_OUTPUT);
    
	%result_hash=(table_hash=>\%target_hash,priority_hash=>\%priority_hash,mirnaname_hash=>\%mirna_hash,result_file=>$output_file, column_names=>\@fields,number_output=>$counter_result);
	return	\%result_hash;
} # sub GetmiRTableViewInfo {



sub GetTargetTableViewInfo {
	my ($field_name, $asse_or_desc,$tmp_database, $tmp_table,$query_database,$tmp_dir,$toolSelection) = @_;#field_name = anything but not mirbase related which indicate the database which it should query ,ie: mirna_human_strict#tmp_dir is the directory of sql files and result files
    my $output_file=$tmp_dir."/query_output.txt";

    close (FH_OUTPUT);#file handle for output file
    open (FH_OUTPUT,">$output_file")||die "Can't open file \n";
    $query_database="gist.".$query_database;
    my $ranked_by="priority";#temperally take priority as ranking
    my %target_hash = ();
    my %mirna_hash = ();#the hash to store mirnaAccession->miRNAAlias
    my %mir2alias_hash=%{retrieve($mir2alias_hash_file)};
	my %result_hash = ();
	my %priority_hash=();
   

	my $statement = "";
	if ($field_name=~'mirbase') {
        print "wrong field name: no mirnabase id allowed";
	}else{
		$statement = "SELECT m.* FROM $query_database m, $tmp_database.$tmp_table t WHERE t.gene = m.refseq_id AND m.priority >= 3 ORDER BY m.$ranked_by $asse_or_desc";
	}
    
    my $dbh = DbSession::GetConnection();
	if (! $dbh) {
		die "There is no connection to the database." . $DBI::errstr;
	}
    my $select = $dbh->prepare($statement) or die "Unable to prepare $statement" . $dbh->errstr();
    $select->execute() or die "Unable to execute $statement.  " . $select->errstr();
    my $nr = $select->rows();#number of rows found
	my @fields=@{$select->{NAME}};#get all column names from the database #id#mirbase_accession#refseq_id#differentdbs#last, priority
    shift @fields;#delete the column of internal id
    print FH_OUTPUT join("\t",@fields),"\n";
    shift @fields;#delete the column of mirna_id
    shift @fields;#delete the column of refseq_id
    pop @fields;#delete the column of priority

    my ($fields_ref,$index_ref)=&get_included_index(\@fields,$toolSelection);#return the fields name to show accoring to tool selection(array), and index of the data in each row
    @fields=@{$fields_ref}; 
    my %indexes=%{$index_ref};#contains the index of clumn=>weight of each column
 
    my @data;#hold the currentline
     my $counter_result=0;
    while(my @data = $select->fetchrow_array){
        #@data= @$row_ref;#get currentline
        my $currentid= shift @data;
        #print "currentId is $currentid \n";
        print FH_OUTPUT join ("\t",@data),"\n";
        my $currentmirna= shift @data;
        my $currenttarget=shift @data;
        my $currentpriority=pop @data;
        $priority_hash{$currenttarget}{$currentmirna}=0;
        my $currentmirnaname = @{$mir2alias_hash{$currentmirna}}[-1];
        $mirna_hash{$currentmirna} = $currentmirnaname;
        my @output=();
        foreach my $key(keys %indexes){
            push @output, $data[$key];
            if($data[$key] eq "yes"){
            $priority_hash{$currenttarget}{$currentmirna}+=$indexes{$key};}
            
        }
        # $priority_hash{$currenttarget}{$currentmirna}=0+$currentpriority;
        if ($priority_hash{$currenttarget}{$currentmirna}>=$priority_def){
        $target_hash{$currenttarget}{$currentmirna}=\@output;
        $counter_result++;
        }else{
            delete $priority_hash{$currenttarget}{$currentmirna};
        }
    
    }
    close(FH_OUTPUT);
    $dbh->disconnect or warn "Disconnection failed : $DBI::errstr\n";
    
	%result_hash=(table_hash=>\%target_hash,priority_hash=>\%priority_hash,mirnaname_hash=>\%mirna_hash,result_file=>$output_file, column_names=>\@fields,number_output=>$counter_result);
 return	\%result_hash;
} # sub GetTargetTableViewInfo {

sub get_included_index{
    my($fields_ref,$toolSelection_ref)=@_;
    my @fields = @{$fields_ref};
    my %toolselection=%{$toolSelection_ref};
    my %indexes;
    my @fields_show=();
    for my $i(0 .. $#fields){
        if(exists $toolselection{$fields[$i]}){
        push @fields_show,$fields[$i];
            if($fields[$i]=~"tarbase"){
            $indexes{$i}=3;}else{
            $indexes{$i}=1;
        }
    } #check if the field is selected through tool selection   
    }
    return (\@fields_show,\%indexes);
}


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
