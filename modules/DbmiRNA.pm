package DbmiRNA;

use DbSession;
use Carp;
use lib "/home/database/perl5/lib/perl5";
#use CGI::Carp;
#use base DeepPrintable;
use Storable;
use Data::Dumper qw(Dumper);
#use List::MoreUtils qw/pairwise/;
use JSON;

my $mir2alias_hash_file="/home/database/projects/gist/systec/mirna/wj/data/miRBase/mir_alias.hash";#this one put the datadir 
#my $priority_def =3;#this is temp testing for setting default priority
#this package contain getTableViewInfo, and by the way generate the query result for down loading
#use constant ID_LOAD_STATEMENT => "SELECT * FROM mirna WHERE id=?";

#use constant GENE_LOAD_STATEMENT => "SELECT * FROM mirna WHERE mirna_name=?";
#my $dbh=DbSession::GetConnection();$sth=$dbh->prepare("SELECT m.* FROM gist.mirna_human_strict AS m");my $rv =$sth->execute();$names=$sth->{NAME},print @$names
sub GetMirTableViewInfo {# this is the function 
	my ($field_name, $asse_or_desc,$tmp_database, $tmp_table,$query_database,$tmp_dir,$toolSelection,$priority_def,$tissue_ref) = @_;#field_name =mirbase _accession or mirbase _name,input type,#add $query_database which indicate the database which it should query ,ie: mirna_human_strict#tmp_dir is the directory of sql files and result files#toolSelection hold hash the tools that has been considered as key $priority_def hold the user selected priority level
    my $output_file=$tmp_dir."/query_output.txt";
   
   ###############begin add selection for tissue########################################
   my $expression_db="human_hpa_normal_tissue";#for trail   
   $expression_db="gist.".$expression_db;
   my @tissue_filter = @{$tissue_ref};
   my $tissue = shift @tissue_filter;
   my $cell_line = shift @tissue_filter;
   my $levels = shift @tissue_filter;
   #my $levels="('Medium','High')";#for trail
   #my $tissue="lung";
   #my $cell_line="";   
   my $subquery="";
   
   if($levels eq ""){
       $subquery="";
   }elsif (!($cell_line eq "") and !($tissue eq "")){
   $subquery=qq[SELECT x.* FROM (SELECT m.* FROM $query_database m INNER JOIN $tmp_database.$tmp_table t ON t.gene=m.mirna_accession) as x INNER JOIN  $expression_db e WHERE x.refseq_id= e.refseq_id AND e.tissue="$tissue" AND e.cell_type = "$cell_line" AND e.level IN $levels AND x.priority >= $priority_def];
   }elsif(!($tissue eq "") and $cell_line eq ""){
   $subquery=qq[SELECT x.* FROM (SELECT m.* FROM $query_database m INNER JOIN $tmp_database.$tmp_table t ON t.gene=m.mirna_accession) as x INNER JOIN  $expression_db e WHERE x.refseq_id= e.refseq_id AND e.tissue="$tissue" AND e.level IN $levels AND x.priority >= $priority_def];
   }elsif($tissue eq "" and !($cell_line eq "")){
     $subquery=qq[SELECT x.* FROM (SELECT m.* FROM $query_database m INNER JOIN $tmp_database.$tmp_table t ON t.gene=m.mirna_accession) as x INNER JOIN  $expression_db e WHERE x.refseq_id= e.refseq_id AND e.level IN $levels AND x.priority >= $priority_def];#this one still need to consider...should it allowed that only cell type present in the query
   }
#example query 
   # select x.* FROM (SELECT m.* FROM gist.mirna_human_strict m INNER JOIN tmp_20150206144843997148558.gene_list__0 t ON t.gene=m.mirna_accession) as x INNER JOIN  gist.human_hpa_normal_tissue e WHERE x.refseq_id= e.refseq_id AND e.tissue="lung" AND e.level IN ('Medium','High');
   # #SELECT m.* FROM gist.mirna_human_strict m WHERE m.priority>=3 AND m.refseq_id = ANY (SELECT DISTINCT t.gene FROM tmp_20150205194447978880162.gene_list__0 t, gist.human_hpa_normal_tissue e WHERE t.gene = e.refseq_id AND e.tissue="lung" AND e.cell_type= "macrophages" AND e.level IN ('Medium','High'));
###############end add selection for tissue########################################
    close (FH_OUTPUT);#file handle for output file
    open (FH_OUTPUT,">$output_file")||die "Can't open file \n";
    $query_database="gist.".$query_database;
    my $ranked_by="priority";#temperally take priority as ranking
    my %target_hash = ();
	my %mirna_hash = ();#the hash to store mirnaAccession->miRNAAlias
    my %mir2alias_hash=%{retrieve($mir2alias_hash_file)};
	my %result_hash = ();	
	my %priority_hash = ();
    my %priority_bay_hash=();
    my %priority_weight=();
    my @genename_array;
	

	my $statement = "";
	if ($field_name=~'mirbase') {
        if($subquery eq ""){
		$statement = "SELECT m.* FROM $query_database m, $tmp_database.$tmp_table t WHERE t.gene = m.mirna_accession AND m.priority >= $priority_def ORDER BY m.$ranked_by $asse_or_desc";#altered
    }else{
    $statement=$subquery;
    }
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
    #   my ($fields_ref,$index_ref)=&get_included_index(\@fields,$toolSelection);#return the fields name to show accoring to tool selection(array), and index of the data in each row
    my ($fields_ref,$index_ref,$weights_ref,$method2name)=&get_included_index(\@fields,$toolSelection);#return the fields name to show accoring to tool selection(array), and index of the data in each row
    #@fields=@{$fields_ref}; 
    my %indexes=%{$index_ref};#contains the index of column=>weight of each column  0 1=>3 3 5 5
    my %weights=%{$weights_ref};###
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
        $priority_weight{$currentmirna}{$currenttarget}=0;#
        $priority_bay_hash{$currentmirna}{$currenttarget}=1;#
        my @output=();
         for my $key(0 .. $#fields){
            if(exists $indexes{$key} ){
            push @output, $data[$key];
            if($data[$key] eq "yes"){
            $priority_hash{$currentmirna}{$currenttarget}+=$indexes{$key};
            $priority_weight{$currentmirna}{$currenttarget}+=$weights{$key};
             
             $priority_bay_hash{$currentmirna}{$currenttarget}*=(1-$weights{$key});
             }#    if($data[$key] eq "yes"){
             }#   if(exists $indexes{$key} ){
            
        }#  for my $key(0 .. $#fields){
        # $priority_hash{$currenttarget}{$currentmirna}=0+$currentpriority;
        if ($priority_hash{$currentmirna}{$currenttarget}>=$priority_def){
        $target_hash{$currentmirna}{$currenttarget}=\@output;
        $counter_result++;
        push @genename_array,$currenttarget;#added
        }# if ($priority_hash{$currentmirna}{$currenttarget}>=$priority_def){ 
        else{ delete $priority_hash{$currentmirna}{$currenttarget};
              delete $priority_bay_hash{$currentmirna}{$currenttarget};  
              delete $priority_weight{$currentmirna}{$currenttarget};  
        }
    
    }# while(my @data= $select->fetchrow_array){
    close(FH_OUTPUT);
    
#	%result_hash=(table_hash=>\%target_hash,priority_hash=>\%priority_hash,mirnaname_hash=>\%mirna_hash,result_file=>$output_file, column_names=>$fields_ref,number_output=>$counter_result);
	%result_hash=(table_hash=>\%target_hash,priority_hash=>\%priority_hash,mirnaname_hash=>\%mirna_hash,result_file=>$output_file, column_names=>$fields_ref,number_output=>$counter_result,genename_array=>\@genename_array,priority_weight=>\%priority_weight,priority_bay_hash=>\%priority_bay_hash, method2name=>$method2name);
	return	\%result_hash;
} # sub GetmiRTableViewInfo {



sub GetTargetTableViewInfo {
	my ($field_name, $asse_or_desc,$tmp_database, $tmp_table,$query_database,$tmp_dir,$toolSelection,$priority_def,$tissue_ref) = @_;#field_name = anything but not mirbase related which indicate the database which it should query ,ie: mirna_human_strict#tmp_dir is the directory of sql files and result files
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
    my %priority_bay_hash=();
    my %priority_weight=();
    my @genename_array;
      ###############begin add selection for tissue########################################
   
   my $expression_db="human_hpa_normal_tissue";#for trail   
   $expression_db="gist.".$expression_db;
   my @tissue_filter = @{$tissue_ref};
   my $tissue = shift @tissue_filter;
   my $cell_line = shift @tissue_filter;
   my $levels = shift @tissue_filter;
   #my $levels="('Medium','High')";#for trail
   #my $tissue="lung";#for trail
   #my $cell_line="";   #for trail
   my $subquery="";
   
   if($levels eq ""){
       $subquery="";
   }elsif (!($cell_line eq "") and !($tissue eq "")){
   $subquery=qq[SELECT m.* FROM $query_database m WHERE m.priority >= $priority_def AND m.refseq_id = ANY (SELECT DISTINCT t.gene FROM $tmp_database.$tmp_table t, $expression_db e WHERE t.gene = e.refseq_id AND e.tissue="$tissue" AND e.cell_type="$cell_line" AND e.level IN $levels)];
   }elsif(!($tissue eq "") and $cell_line eq ""){
   $subquery=qq[SELECT m.* FROM $query_database m WHERE m.priority >= $priority_def AND m.refseq_id = ANY (SELECT DISTINCT t.gene FROM $tmp_database.$tmp_table t, $expression_db e WHERE t.gene = e.refseq_id AND e.tissue="$tissue" AND e.level IN $levels)];
   }elsif($tissue eq "" and !($cell_line eq "")){
    $subquery=qq[SELECT m.* FROM $query_database m WHERE m.priority >= $priority_def AND m.refseq_id = ANY (SELECT DISTINCT t.gene FROM $tmp_database.$tmp_table t, $expression_db e WHERE t.gene = e.refseq_id AND e.cell_type="$cell_line" AND e.level IN $levels)];#this one still need to consider...should it allowed that only cell type present in the query
   }
#example query 
#SELECT m.* FROM gist.mirna_human_strict m WHERE m.priority>=3 AND m.refseq_id = ANY (SELECT DISTINCT t.gene FROM tmp_20150205194447978880162.gene_list__0 t, gist.human_hpa_normal_tissue e WHERE t.gene = e.refseq_id AND e.tissue="lung" AND e.level IN ('Medium','High'));
###############end add selection for tissue########################################

	my $statement = "";
	if ($field_name=~'mirbase') {
        print "wrong field name: no mirnabase id allowed";
	}else{
		if($subquery eq ""){
        $statement = "SELECT m.* FROM $query_database m, $tmp_database.$tmp_table t WHERE t.gene = m.refseq_id AND m.priority >= $priority_def ORDER BY m.$ranked_by $asse_or_desc";}else{
    $statement = $subquery;
    }
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

    #my ($fields_ref,$index_ref)=&get_included_index(\@fields,$toolSelection);#return the fields name to show accoring to tool selection(array), and index of the data in each row
    
    my ($fields_ref,$index_ref,$weights_ref,$method2name)=&get_included_index(\@fields,$toolSelection);#return the fields name to show accoring to tool selection(array), and index of the data in each row
    #@fields_final=@{$fields_ref}; 
    my %indexes=%{$index_ref};#contains the index of clumn=>weight of each column
 
    my %weights=%{$weights_ref};###
    my @data;#hold the currentline
     my $counter_result=0;
    while(my @data = $select->fetchrow_array){
        #@data= @$row_ref;#get currentline
        my $currentid= shift @data;
        #print "currentId is $currentid \n";
        print FH_OUTPUT join ("\t",@data),"\n";
        my $currentmirna= shift @data;
        my $currenttarget=shift @data;
        my $currentpriority=pop @data;# this is the fake priority 
        $priority_hash{$currenttarget}{$currentmirna}=0;
        my $currentmirnaname = @{$mir2alias_hash{$currentmirna}}[-1];
        $mirna_hash{$currentmirna} = $currentmirnaname;
        $priority_weight{$currenttarget}{$currentmirna}=0;#
        $priority_bay_hash{$currenttarget}{$currentmirna}=1;#
        my @output=();
        for my $key(0 .. $#fields){
            if(exists $indexes{$key} ){
            push @output, $data[$key];
            if($data[$key] eq "yes"){
            $priority_hash{$currenttarget}{$currentmirna}+=$indexes{$key};
            $priority_weight{$currenttarget}{$currentmirna}+=$weights{$key};
             $priority_bay_hash{$currenttarget}{$currentmirna}*=(1-$weights{$key});
        }
        }
        }
        # $priority_hash{$currenttarget}{$currentmirna}=0+$currentpriority;
        if ($priority_hash{$currenttarget}{$currentmirna}>=$priority_def){
        $target_hash{$currenttarget}{$currentmirna}=\@output;
        $counter_result++;
        }else{
            delete $priority_hash{$currenttarget}{$currentmirna};
            delete $priority_bay_hash{$currenttarget}{$currentmirna};  
            delete $priority_weight{$currenttarget}{$currentmirna};  
        }
    
    }
    close(FH_OUTPUT);
    $dbh->disconnect or warn "Disconnection failed : $DBI::errstr\n";
    my @genename_array=keys(%priority_hash);
    
	%result_hash=(table_hash=>\%target_hash,priority_hash=>\%priority_hash,mirnaname_hash=>\%mirna_hash,result_file=>$output_file, column_names=>$fields_ref,number_output=>$counter_result,genename_array=>\@genename_array,priority_weight=>\%priority_weight,priority_bay_hash=>\%priority_bay_hash, method2name=>$method2name);
 return	\%result_hash;
} # sub GetTargetTableViewInfo {

sub get_included_index{#get the index of columns (fields of tools) that need to be included in the output html
    my($fields_ref,$toolSelection_ref)=@_;
    my @fields = @{$fields_ref};
    my %toolselection=%{$toolSelection_ref};
    my %indexes;
    my %weights;
    my @fields_show=();
    #################
#    for my $i(0 .. $#fields){
#        if(exists $toolselection{$fields[$i]}){
#        push @fields_show,$fields[$i];
#           if( $fields[$i]=~/base/ ){
#              $indexes{$i}=3;}else{
#            $indexes{$i}=1;
#                   }
#    } #check if the field is selected through tool selection   
#    }
##matrix of the weight(PPV), and name for each prediction name    
$json_hm = '[
{
    "Prediction_method":"9606_Evidence_SE_mirtarbase",
    "name":"mirtarbase_SE",
    "PPV":1
  },
{
    "Prediction_method":"9606_Evidence_WK_mirtarbase",
    "name":"mirtarbase_WK",
    "PPV":1
  },
  {
    "Prediction_method":"9606_tarbase",
    "name":"tarbase",
    "PPV":1
  },
  {
    "Prediction_method":"targetminer_9606_targetminer",
    "name":"targetminer",
    "PPV":0.0167237749
  },
  {
    "Prediction_method":"9606_3utr_mirtar",
    "name":"mirtar_3utr",
    "PPV":0.0206829612
  },
  {
    "Prediction_method":"9606_5utr_mirtar",
    "name":"mirtar_5utr",
    "PPV":0.0115659483
  },
  {
    "Prediction_method":"9606_access_2_5_paccmit",
    "name":"PACCMIT_TOP",
    "PPV":0.0237869338
  },
  {
    "Prediction_method":"9606_access_cons_2_5_paccmit",
    "name":"PACCMIT_Con_TOP",
    "PPV":0.049760814
  },
  {
    "Prediction_method":"9606_access_cons_paccmit",
    "name":"PACCMIT_Con",
    "PPV":0.0477901154
  },
  {
    "Prediction_method":"9606_access_paccmit",
    "name":"PACCMIT",
    "PPV":0.0223343044
  },
  {
    "Prediction_method":"9606_all_mirtar",
    "name":"mitar",
    "PPV":0.0169867785
  },
  {
    "Prediction_method":"9606_broadly_targetScan",
    "name":"targetScan_broadly",
    "PPV":0.064775812
  },
  {
    "Prediction_method":"9606_cds_mirtar",
    "name":"mirtar_cds",
    "PPV":0.0147161692
  },
  {
    "Prediction_method":"9606_Conservation_0_targetrank",
    "name":"targetrank",
    "PPV":0.049806495
  },
  {
    "Prediction_method":"9606_Conservation_1_targetrank",
    "name":"targetrank_Con",
    "PPV":0.0829436377
  },
  {
    "Prediction_method":"9606_conserved_targetScan",
    "name":"targetscan_conserve",
    "PPV":0.0604318197
  },
  {
    "Prediction_method":"9606_cons_paccmit_cds",
    "name":"PACCMIT_CDS_Con",
    "PPV":0.0158181968
  },
  {
    "Prediction_method":"9606_cons_paccmit",
    "name":"PACCMIT_Con_low",
    "PPV":0.0442394467
  },
  {
    "Prediction_method":"9606_microcosm_mirna2target",
    "name":"microcosm",
    "PPV":0.0267181903
  },
  {
    "Prediction_method":"9606_microrna_org_conserved",
    "name":"microrna.org_conserved",
    "PPV":0.0394944273
  },
  {
    "Prediction_method":"9606_microrna_org_non_conserved",
    "name":"microrna.org",
    "PPV":0.0042416243
  },
  {
    "Prediction_method":"9606_mirdb",
    "name":"mirdb",
    "PPV":0.0344012945
  },
  {
    "Prediction_method":"9606_mirnamap_2_1_1",
    "name":"mirnamap2_2tool",
    "PPV":0.0325749385
  },
  {
    "Prediction_method":"9606_mirna_2_2_1",
    "name":"mirnamap2_2tools_strict",
    "PPV":0.0423757853
  },
  {
    "Prediction_method":"9606_nfe_-15_nm_0.1_reptar",
    "name":"reptar_TOP",
    "PPV":0.0163132626
  },
  {
    "Prediction_method":"9606_nonconserved_targetScan",
    "name":"targetScan_non_conserve",
    "PPV":0.0468181263
  },
  {
    "Prediction_method":"9606_P_0.5CDS_eimmo",
    "name":"eimmo_CDS_TOP",
    "PPV":0.0188979846
  },
  {
    "Prediction_method":"9606_P_0.5_eimmo",
    "name":"eimmo_TOP",
    "PPV":0.0505244542
  },
  {
    "Prediction_method":"9606_P_0_eimmo",
    "name":"eimmo",
    "PPV":0.0185273747
  },
  {
    "Prediction_method":"9606_paccmit_cds",
    "name":"PACCMIT_CDS",
    "PPV":0.014424595
  },
  {
    "Prediction_method":"9606_paccmit",
    "name":"PACCMIT_low",
    "PPV":0.0211921128
  },
  {
    "Prediction_method":"9606_pictar_mammal_conserved",
    "name":"pictar",
    "PPV":0.0475667829
  },
  {
    "Prediction_method":"9606_pictar_most_conserved",
    "name":"pictar_TOP",
    "PPV":0.0770642202
  },
  {
    "Prediction_method":"9606_pita_no_flank_TOP",
    "name":"pita_TOP",
    "PPV":0.0547144877
  },
  {
    "Prediction_method":"9606_pita_no_flank_ALL",
    "name":"pita_strict_All",
    "PPV":0.0192610164
  },
  {
    "Prediction_method":"9606_sens_all_targetspy",
    "name":"targetspy_sensitive",
    "PPV":0.0140366651
  },
  {
    "Prediction_method":"9606_sens_seed_targetspy",
    "name":"targetspy_seed",
    "PPV":0.0303612868
  },
  {
    "Prediction_method":"9606_spec_seed_targetspy",
    "name":"targetspy_specific",
    "PPV":0.0301555665
  },
  {
    "Prediction_method":"9606_TG0.7_CDS_microT",
    "name":"microT_CDS_TOP",
    "PPV":0.0283751419
  },
  {
    "Prediction_method":"9606_TG0.7_microtv4_microT",
    "name":"microT4_TOP",
    "PPV":0.076309795
  },
  {
    "Prediction_method":"9606_TG0_CDS_microT",
    "name":"microT_CDS",
    "PPV":0.0158571958
  },
  {
    "Prediction_method":"9606_TG0_microtv4_microT",
    "name":"microT4",
    "PPV":0.0149033578
  }
]';
#my %params = map { $_ => 1 } @badparams;
#if(exists($params{$someparam})) { ... }
$dbs = decode_json($json_hm);
my %method2name;
my %method2PPV;

for my $href ( @$dbs ) {
       my $method = $href->{"Prediction_method"};   
         $method2name{$method}= $href->{"name"} ;
         $method2PPV{$method}= $href->{"PPV"} ;
}
#build hashes to record method2name and method2PPV
     for my $i(0 .. $#fields){
        if(exists $toolselection{$fields[$i]}){
        push @fields_show,$fields[$i];
            if( $fields[$i]=~/base/ ){
            $indexes{$i}=3;}else{
            $indexes{$i}=1;
        }
        $weights{$i}=$method2PPV{  $fields[$i] };
        #print $fields["13"].":".$weights{"13"};
    } #check if the field is selected through tool selection   
    }   
    
    #return (\@fields_show,\%indexes);
    return (\@fields_show,\%indexes,\%weights,\%method2name);#field to show(predictions),$indexes predictions->1or 3, weight, predictions to
}

sub multiply{
@a = @{$_[0]};
@b = @{$_[1]};
@x = pairwise { $a * $b } @a, @b;
return @x;
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
