package IdMapper;
use Carp;
use Storable;
use Data::Dumper qw(Dumper);

##########################################
##
## Document   : IdMapper.pm
## Created on : Oct 15th, 2014
## Author     : Venkata P. Satagopam (venkata.satagopam@embl.de) jiali.wang@uni.lu
## Description: It mapps/ converts different ids to ensembl gene ids ..it is file based /it convert ensembl gene ids to refseq Id
##
##########################################
my $map_dir ="/home/database/projects/biocompendium3/data/"; 
my $transform_hash_dir="/home/database/projects/gist/systec/mirna/wj/data/" ;#this one put the datadir 
sub get_ensembl_genes {
    my ($org, $list, $id_doc_type) = @_;
    my @list = @$list;
#print "list : @list<br>";	
    my @ensembl_genes = ();
#	if ($id_doc_type ne 'ensembl_gene_id') {
    my $file = $map_dir . $org . "/biomart/ensembl_gene_id__". $id_doc_type;
#print "from IdMapper<br>org : $org<br>primary_org:$primary_org<br>";
#print STDERR "file : $file<br>";
    my %map_hash = ();
    my $line = "";
    close(FH);
    if (open(FH, "$file")) {
        while(<FH>) {
            $line = $_;
            chomp($line);
            my ($ensg, $second_id) = split("\t", $line);
            $map_hash{$second_id} = $ensg;			
        } # while(<FH>) {
    } # if (open(FH, "$file")) {
    close(FH);
#my @keys = keys %map_hash;
#my $keys_size = @keys;
#print "keys_size : $keys_size<br>";
    foreach my $e (@list) {
#		chomp($e);
#print "protein : $e<br>";
        if ($map_hash{$e}) {
            my $id = $map_hash{$e};
#print "gene : $id<br>";
            push @ensembl_genes, $id;
        } # if ($map_hash{$e}) {
    } # foreach my $e (@list) {

    @ensembl_genes = &nonRedundantList(\@ensembl_genes);
#	} # if ($id_doc_type ne 'ensembl_gene_id') {
#	else {
#		@ensembl_genes = @list;
#	}
return @ensembl_genes;

} # sub get_ensembl_genes {


sub get_refseq_genes {#this is the general function to get the unified IDs ,in short the refseqs and miRNA mature RNA accession
    my ($org, $list, $id_doc_type) = @_;#organism, $list=ref of the input gene list,$id_doc_type
    #print "current org is $org;";#testing
    #print "enter get_refseq_genes\n";#testing
    my @list = @$list;
    #print "current list before transform is @list";#testing
    #print "current id_doc is $id_doc_type\n";#testing
    
    my $tax_ID;
    my %transform_hash;
    if($org eq 'human'){$tax_ID='9606'}else{$tax_ID='10090';}
    #print "tax id is $tax_ID";
    my @final_genes = ();
    my $transform_hash_file;
    my $route=1;#a variable indicate that which route to take.... if it is 1(the transform hash is 1->1string hash),if it is 0, indicate that it is a 1->@ids hash#if it is 3 indicate a special case for MI accession
    if ($id_doc_type eq 'refseq_id') {
		#print "nothing to change !";
        @final_genes=@list;
        return @final_genes;
    } 
    elsif ($id_doc_type eq 'mirbase_accession') {
        #there is two possibility:1 it is a mature ID;2 it is a MI accession
        #don't need transformation of mirbase_accession so do nothing
        $route=2;#do nothing and jump all the transform procedure
        @final_genes=@list;

    }  
    elsif($id_doc_type eq 'mirbase_name'){
        $transform_hash_file=$transform_hash_dir.'miRBase/mirAlias2Accession.hash';
        $route=1;
        
    }
    elsif($id_doc_type eq 'ensembl_gene_id'){
        $transform_hash_file=$transform_hash_dir.'annotations/'.$tax_ID.'_ensg2refseqs.hash';
        $route=0;
    }
    elsif($id_doc_type eq 'ensembl_transcript_id'){
        $transform_hash_file=$transform_hash_dir.'annotations/'.$tax_ID.'_ensembl_transcriptID2refseqID.hash';

    }
    elsif($id_doc_type eq 'entrezgene'){
        $transform_hash_file=$transform_hash_dir.'annotations/'.$tax_ID.'_enterz2refseqs.hash';
        $route=0;
        
    }

    elsif($id_doc_type eq 'hgnc_symbol'){
        $transform_hash_file=$transform_hash_dir.'annotations/'.$tax_ID.'_rnaGeneName2refseqs.hash';
        $route=0;
    }
    else{#if can't find direct match first match to ensembl gene ids and then transform to refseqIDs first match to ensembl_gene_id
        @list = &get_ensembl_genes($org,$list,$id_doc_type);
        $transform_hash_file=$transform_hash_dir.'annotations/'.$tax_ID.'_ensg2refseqs.hash';
        $route=0;
    }
    #print "transform hash is $transform_hash_file\n";#testing
    if($route!=2){#if route=2 there is no need for transformation
    %transform_hash=%{retrieve($transform_hash_file)};
    if($route==0){
        foreach my $e (@list) {

            if (exists $transform_hash{$e}) {
                my @id = @{$transform_hash{$e}};
            
                push @final_genes, @id;
            } # if ($map_hash{$e}) {
        } # foreach my $e (@list) {
	} else{
		#print "enter route 1\n";
		 foreach my $e (@list) {
#		chomp($e);
#print "protein : $e<br>";
        if (exists $transform_hash{$e}) {
            my $id = $transform_hash{$e};            
            #print "gene : $id<br>";
            push @final_genes, $id;
            } # if ($map_hash{$e}) {
        } # foreach my $e (@list) {
		}#else
    }#if($route!=2){#if route=2 there is no need for transformation
    if($id_doc_type eq 'mirbase_accession'||$id_doc_type eq "mirbase_name"){#there is a possibility that @finalgenes contains MIaccession
     my @final_accessions=();
        foreach my $ac (@final_genes){
            if  ($ac=~"MIMAT"){#this is a mature Id
                push @final_accessions,$ac;
                #print "find mature ID $ac<br>";
            }else{#this is not a mature ID but a id start with MI
                my @current_acc=&get_mature_miRAccessions($ac);
                push @final_accessions,@current_acc;

            }  #else
    }#foreach
    @final_genes = @final_accessions;
}#there is a possibility that @finalgenes contains MIaccession
    @final_genes = &nonRedundantList(\@final_genes); 
if(@final_genes){return @final_genes;}else{print "Please recheck the selected id type !\n";}
} # sub get_refseq_genes {

sub get_mature_miRAccessions {
    my $miAccession = pop(@_);
    my @all;
    my $line;
    my %mi2mimat_hash = ();
    my $mi2mimat_hash_file=$transform_hash_dir.'miRBase/mi2mimat.hash'; 
    if (-e $mi2mimat_hash_file) { 
        #print "File Exists!";
         %mi2mimat_hash=%{retrieve($mi2mimat_hash_file)};
         if(exists $mi2mimat_hash{$miAccession}){ 
         return @{$mi2mimat_hash{$miAccession}};
         }else{return $miAccession;}        
    }else{
    my  $mi2mimat_filename = $transform_hash_dir.'miRBase/mirbase_mi_mimat.txt';
    if(open (MI2MIMAT,$mi2mimat_filename)){
        @all=<MI2MIMAT>;
        shift @all;
        close (MI2MIMAT);
        while (@all){
            $line =shift @all;
            chomp ($line);
            if($line){
                my @current= split("\t",$line);
                my $miaccession= shift @current;
                my @currentMIMATs;
                shift @current;
                shift @current;
                shift @current;
                my $i;
                for ($i=0;$i<@current;$i+=3){
                    push @{$mi2mimat_hash{$miaccession}}, $current[$i];
                }# foreach my $cell (@current){
            } #if($line){
        }# while (@all){
        store \%mi2mimat_hash,$mi2mimat_hash_file;
        if(exists $mi2mimat_hash{$miAccession}){ 
        return @{$mi2mimat_hash{$miAccession}};
        }else{return $miAccession;}      
    }#if file exist
    else{print "mi2mimiat file does not exist\n";}
    }#build the mi2mimat_hash_file
} # sub get_mature_miRAccessions {

sub nonRedundantList{
    my $val = shift;
    my @val=@$val;                                                
    my %cpt;
    foreach (@val){                                               
        $cpt{$_}++;                                                 
    }                                                             
    return keys %cpt;
} # sub redundantList{
