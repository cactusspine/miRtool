#!/usr/bin/perl -w

#################################################################
## Developed by Venkata P. Satagopam venkata.satagopam@embl.de##
#               Jiali Wang jialimwang@gmail.com                ##
## Disclaimer: Copy rights reserved by EMBL, please contact    ## 
## Venkata Satagopam prior to reuse any part of this code      ##
#################################################################

use strict;
use lib "/home/database/projects/gist/systec/modules";

use IdMapper;
use DbmiRNA;
use Math::Combinatorics;
use List::Compare;
use Data::Dumper;

use CGI;#just imports the functions and variables that CGI.pm lumps in the "standard" export group. That includes things like cookie(), header(), param(), blah blah blah
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

my $q    = new CGI;
my %q = %$q;
my $search = $q->param( "search" );
my $position = $q->param("pos");
my $sort_by_field_name = $q->param("sort");
my $asc_or_desc = $q->param("ad");
my $session = $q->param("session");
my $permanent_session = $q->param("permanent_session");
my $text_area_ids = $q->param("text_area_ids");
my $ids_file = $q->param("ids_file");
my $input_type = $q->param("Category1");
my $output_type = $q->param("SubCat1");
my $gene_name = $q->param("gene_name");
my $section = $q->param("section");
my $org = $q->param("org");
#$org = 'human';#for testing
#print "organism from input is $org";
my $list = $q->param("list");
#tissue filter###
my $tissue = $q->param("tissue");
my $cell_type = $q->param("cell_type");
my $gene_expression = $q->param("gene_expression");
if(!$tissue) {
    $tissue = "";
}
if(!$cell_type) {
    $cell_type = "";
}if(!$gene_expression) {
    $gene_expression = "";
}
my  @tissuefilter = ( $tissue, $cell_type,$gene_expression );
##End tissue filter####
my @toolselection = $q->param("toolselection");#selectedtools
my %toolselection;#
my $priority_user=$q->param("priority_user");
if(!$position) {
    $position = "";
}
if(!$search) {
    $search = "";
}
if(!$sort_by_field_name) {
    $sort_by_field_name = "";
}
if(!$asc_or_desc) {
    $asc_or_desc = "";
}
if(!$session) {
    $session = "";
}
if(!$permanent_session) {
    $permanent_session = "";
}
if(!$gene_name) {
    $gene_name = "";
}
if(!$section) {
    $section = "";
}
if(!$org) {
    $org = "human";#for testing
}
if(!$input_type) {
    $input_type = "mirbase_accession";
}
if(!$output_type) {
    $output_type = "";
}
if(!$text_area_ids) {
    $text_area_ids = "";#for testing
}
if(!$priority_user) {
    $priority_user = 3;#for testing
}
if(!@toolselection){
    #print "Please Select at least one tool!\n";
    #die "no tool selected";
}else{
    %toolselection = map {$_=>1} @toolselection;
}#check if it is empty #0110
my $host_name = "http://bio1.uni.lu:8081";
#my $host_name = "http://rschneider.embl.de/";
#my $URL_project = $host_name . "/biocompendium/";
my $URL_project = $host_name . "/";
my $URL_cgi = $host_name . "/cgi-bin/systec.cgi";
#my $STITCH_URL = "http://stitch.embl.de";
#my $chemistry_url = $URL_project . "/temp/structure/";
#my $pubchem_url = "http://pubchem.ncbi.nlm.nih.gov/summary/summary.cgi?cid=";
#my $dasty2das_client = "http://www.ebi.ac.uk/dasty/client/ebi.php";
#my $outPutDir = "/var/www/html/rschneider/systec/database/temp/";
my $outPutDir = "/home/database/projects/gist/httpd/htdocs/mirna/database/temp/";
#my $cgi_dir = "/var/www/cgi-bin/";
my $cgi_dir = "/home/database/projects/gist/httpd/cgi-bin/";
my $biocompendium_perl = $cgi_dir . "biocompendium_perl/";
my $biocompendium_R = $cgi_dir . "biocompendium_R/";
my $uniprot_uri = "http://uniprot.org/uniprot";
my $hyper_link_img = "hyperlink.png";
my $hyper_link_flag_img = "flag.png";
my $hyper_link_img_width = '12';
my $hyper_link_img_height = '12';
my $table_width = '1200';
print $q->header( "text/html" ),
$q->start_html( -title=>'Systec:FANCI database',
    -auther=>'Venkata P. Satagopam (venkata.satagopam@embl.de)',
    -meta=> {keywords=>'bioCompendium EMBL Venkata P. Satagopam venkata.satagopam@embl.de'},
    -style=>{-src=>['http://bio1.uni.lu:8081/mirna/database/style/systecnew.css']},
    -script=>[
        
        {-language=>'JAVASCRIPT',
            -src=>'http://rschneider.embl.de/systec/database/javascript/dynamic_file_upload.js'},
        {-language=>'JAVASCRIPT',
            -src=>'http://rschneider.embl.de/systec/database/javascript/id_type.js'},

        {-language=>'JAVASCRIPT',
            -src=>'http://rschneider.embl.de/systec/database/javascript/systec.js'},
        {-language=>'JAVASCRIPT',
            -src=>'http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js'},
         {-language=>'JAVASCRIPT',
            -src=>'http://bio1.uni.lu:8081/mirna/database/javascript/systecnew.js'},
        {-language=>'JAVASCRIPT',
            -src=>'http://bio1.uni.lu:8081/mirna/database/javascript/sorttable.js'}
    ]
);

# this line include the form action, cgi script etc, ...very nice one
my $form_name = "systec";
my $method = "POST";
my $action = "/cgi-bin/systec.cgi";
my $encoding = "multipart/form-data";
#print $q->startform($method, $action, $encoding, "name=\"$form_name\"");

my %tax_mappings = (
    9606  => 'human',
    10090 => 'mouse',
    4932  => 'yeast',

    'human'  => 9606,
    'mouse'  => 10090,
    'yeast'  => 4932
); 		     


my %org_mappings = (
    'human' => 'Homo_sapiens',
    'mouse' => 'Mus_musculus',
    'yeast' => 'Saccharomyces_cerevisiae',
); 		     

my %tool_mappings=(
 '9606_3utr_mirtar' => 'miRTar',
 '9606_access_cons_paccmit' =>	'PACCMIT',
 '9606_cons_paccmit_cds' =>  'PACCMIT-CDS',
'9606_Conservation_1_targetrank' => 'TargetRank',
'9606_Evidence_SE_mirtarbase' => 'mirTarbase-Strong Evidence',
'9606_Evidence_WK_mirtarbase' => 'MirTarbase-All Evidence',
'9606_microcosm_mirna2target' => 'microcosm',
'9606_microrna_org_conserved' => 'microRNA.org_Conserved',
'9606_mirdb' => 'miRDB',
'9606_mirna_2_2_1' => 'TargetScan_Conserved',
'9606_nfe_-15_nm_0.1_reptar' => 'Reptar_strict',
'9606_P_0.5_eimmo' => 'EIMMO_conserved',
'9606_pictar_most_conserved' => 'Pictar_Conserved',
'9606_pita_no_flank_TOP' => 'PITA_Top',
'9606_spec_seed_targetspy' => 'Targetspy_strict',
'9606_tarbase' => 'Tarbase',
'9606_TG0.7_CDS_microT' => 'MicroT-cds',
'targetminer_9606_targetminer' => 'targetminer'

);

#	if($search && $search ne "search...") {
#                &keyword_search($search);
#        }  
if ($section eq "biodb") {
    &table_view($position, $session, $input_type, $sort_by_field_name, $asc_or_desc);
}
#	elsif($permanent_session eq "yes") {
#		&process_genelists_permanent_session($session);
#	}
else {	
    my $result = &process_genelists();
}

print $q->endform;
print $q->end_html;

sub process_genelists {
# session directory
    my $session = `date +%Y%m%d%k%M%S%N`;
    $session =~ s/ //g;
    chop($session);
    $session = "tmp_" . $session;
    my $session_dir = $outPutDir . "sessions/" . $session . "/";
#print "session_dir : $session_dir\n";
    `rm -rf $session_dir; mkdir $session_dir; chmod -R 777 $session_dir`;

# mysql file 
    close(FH_MYSQL);
    my $mysql_file = $session_dir . "/mysql_file.sql"; 
    open(FH_MYSQL, ">$mysql_file");
    print FH_MYSQL "CREATE DATABASE IF NOT EXISTS $session;\n";
    print FH_MYSQL "USE `$session`;\n";

    my @all_genes = ();
    #my $org = "human";

    my @gene_list = ();
    if ($text_area_ids) {
        my @temp_gene_list = split("\n", $text_area_ids);
        foreach my $gene (@temp_gene_list) {
            if (($gene ne "")&&($gene=~/[a-zA-Z0-9-_]+/)) {
                chomp($gene);	
                $gene=~s/\n|\r| //g;
                if (($gene!~/DELETE/i)&&($gene!~/DROP/i)) {
                    push @gene_list, $gene;
                }
#print "-$gene-<br>";
            }

        } # foreach my $gene (@temp_gene_list) {

    @gene_list = &nonRedundantList(\@gene_list);
#print "Original gene list: @gene_list\n";#testing
    @gene_list = &IdMapper::get_refseq_genes($org,\@gene_list,$input_type);#transform gene lists into refseq id or miRNA_Accession id
    }
    else {#not reading the text from text area but input file
        my $file = $ids_file;
#print "input_type : $input_type, org : $org, file : $file<br>";
        @gene_list = &get_gene_list($org, $file, $input_type, $session_dir);
        @gene_list = &IdMapper::get_refseq_genes($org,\@gene_list,$input_type);
#print "gene_list : @gene_list<br>";
    }
#print "gene_list final : @gene_list<br>";

    my $i=0;
    my $fh = "";
    my $gene_list_str = "";
    my $table_name = "";
    my $create_table_string = "";
    my $list_name = "gene_list";
    if (@gene_list) {
        ### create gene list table
        $table_name = $list_name . "__" . $i;
        $create_table_string = &create_table($table_name, \@gene_list);
    print FH_MYSQL "$create_table_string";

    ### create gene list file
    $fh = $session_dir . "$table_name" . ".txt";
    close (FH);
    open(FH,">$fh");
    $gene_list_str = join("\n", @gene_list);
    print FH "$gene_list_str\n";
    close (FH);
} # if (@gene_list) {
else{print "the gene list is empty!\n"};
#print "</table><br></td>";
#print "</tr>";

close(FH_MYSQL);
#	system("/usr/bin/mysql -u srk -psrk -h 10.79.5.221 < $mysql_file");
system("/usr/bin/mysql -u srk -psrk < $mysql_file");
&table_view(0, $session, $input_type, 'mirna_name', 'desc',$org,$session_dir,\@gene_list);#position, $session, $input_type,$sort_by_field_name,$asc or desc
} # sub process_genelists {


sub get_gene_list {
    my ($org, $file, $input_type, $session_dir) = @_;
    my $file_name = "";
    if ($file=~m/^.*(\\|\/)(.*)/){ # strip the remote path and keep the file_name 
        $file_name = $2;
    }
    else {
        $file_name = $file;
    }
    my $dir_local_file = $session_dir . "gene_list__0";
#print "dir_local_file : $dir_local_file<br>";
    #

    my @ensembl_genes = (); 
    my @id_list = ();
    while(<$file>) {
        my $id = $_;

        my @tmp_ids = split("\n|\r", $id);
        foreach my $tmp_id (@tmp_ids) {
            if (($tmp_id) && ($tmp_id!~/DELETE/i)&&($tmp_id!~/DROP/i)) {
                push @id_list, $tmp_id if $tmp_id;
            }
        } # foreach ...
    }
#print "id_list : @id_list<br>";
#	if ($input_type eq "pseudogene_id" || $input_type eq "mirbase_name" || $input_type eq "mirbase_id" || $input_type eq "long_ncrna_id" || $input_type eq "antisense_rna_id" || $input_type eq "sirna_id" || $input_type eq "snorna_id" || $input_type eq "snrna_id" || $input_type eq "trna_id" || $input_type eq "rrna_id" || $input_type eq "pirna_id") {
#		@ensembl_genes = @id_list;
#	} # if ($input_type eq "ensembl_gene_id" ) {
#	else {
#		@ensembl_genes = &IdMapper::get_ensembl_genes($org, \@id_list, $input_type, $primary_org);
#	} # else 
#print "ensembl_genes : @ensembl_genes<br>";
    @id_list = &IdMapper::get_refseq_genes($org,\@id_list,$input_type);
    @id_list = &nonRedundantList(\@id_list);
    return @id_list;
} # sub get_gene_list {


sub table_view {
    my ($position, $session, $input_type, $sort_by_field_name, $asc_or_desc,$org,$session_dir,$gene_list_ref) = @_;#altered added genelist ref
    my $session_output_url=$host_name."/mirna/database/temp/sessions/".$session."/query_output.txt";
    my $list_name = "gene_list__0";
    #my $org = "human";
    my $section="biodb";
    my $query_db;#

    if($org eq 'human'){$query_db = "mirna_human_strict";}#
    #  if($org eq 'mouse'){}#not realized yet

    my $result_hash = undef;
    my %result_hash;
    my %table_hash;

    if($input_type eq "mirbase_name"||$input_type eq "mirbase_accession") {
        $result_hash = &DbmiRNA::GetMirTableViewInfo($input_type, $asc_or_desc, $session, $list_name,$query_db,$session_dir,\%toolselection,$priority_user,\@tissuefilter);#field_name,asse or desc, $temp_database,$tmp_table,$query_database
        #%result_hash=%$result_hash;
        # %table_hash=%{$result_hash->{'mirna_hash'}};
    }
    else {
        $result_hash = &DbmiRNA::GetTargetTableViewInfo($input_type, $asc_or_desc, $session, $list_name,$query_db,$session_dir,\%toolselection,$priority_user,\@tissuefilter);#pass the tool selection to file
       
        #%table_hash=%{$result_hash->{'target_hash'}};
    }
    %result_hash=%$result_hash;
    %table_hash=%{$result_hash->{'table_hash'}};
    my @field_names=@{$result_hash->{'column_names'}};
    my $output_file_path=$result_hash->{'result_file'};
    my $number_of_output=$result_hash->{'number_output'};

    my @keys = keys %table_hash;

    @keys = sort @keys;
    my $size = scalar(@keys);
    my $input_nr= scalar(@{$gene_list_ref});#added
    my $db_nr = scalar(@toolselection);
    ##print what's before the fact sheet
    my $heredoc = <<"HEREDOCEND";
    <div id="page">
    <header role="banner">        		
        		<h1>Systec: Integrated Data Portal for miRNA Target Prediction
                    <br>
               </h1>      
        	</header>
            <nav class="dark">
                <li><a href="/mirna/database/home.html">Home</a></li>
                 <li><a href="/mirna/database/index.html">Query</a></li>
                 <li><a href="/mirna/database/help.html">Help</a></li>
                 <li><a href="/mirna/database/about.html">About</a></li>
                 <li><a href="/mirna/database/links.html">Link</a></li>
                 <input class="nav-search" type="text" placeholder="Search..."/>
        </nav>
            	<div id="main">
        		<div id="pagecontent" >                    
                         <table id="factsheet" width="50%" cellpadding="4px" cellspacing="0" >
HEREDOCEND
    #note that fore HEREDOC the END word must be at the starting of the script
     print $heredoc;

    ##################################
    if(($input_type eq "mirbase_name")||($input_type eq "mirbase_accession")) {
        #############################################
        $heredoc = <<"HEREDOCEND";
                                     <tr>
                                 <td>Number of Input microRNA</td><td>$input_nr</td>
                             </tr>
                             <tr>
                                 <td>Number of Analysed microRNA</td><td>$size</td>
                             </tr>
                            
                                 <tr>
                                 <td>Number of Prediction Tools/EvidenceDBs</td><td>$db_nr</td>
                             </tr>
                                 <tr>
                                 <td>Advanced Parameters(Minimum Priority)</td><td>$priority_user</td>
                             </tr>
                              <tr>
                                 <td>Number of Output mRNAs</td><td>$number_of_output<a href=\"$session_output_url\"><b>   download Result</b></a><br><img alt="expand" src='http://bio1.uni.lu:8081/mirna/database/images/plus.gif' id="expand" class="toclick"> Expand All <img alt="collapse" src='http://bio1.uni.lu:8081/mirna/database/images/minus.gif' id="collapse" class="toclick">Collapse All
                                 </td>
                             </tr>
                         </table><!--#factsheet-->
<br>
<ul class="accordion">
HEREDOCEND
         print $heredoc;
        ################################################
        #print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>No. of miRNAs : $size</b></font><br></td>\n";
    }
    else {
        ##################################
                $heredoc = <<"HEREDOCEND";
                                     <tr>
                                 <td>Number of Input mRNA</td><td>$input_nr</td>
                             </tr>
                             <tr>
                                 <td>Number of Analysed mRNA</td><td>$size</td>
                             </tr>

                                 <tr>
                                 <td>Number of Prediction Tools/EvidenceDBs</td><td>$db_nr</td>
                             </tr>
                                 <tr>
                                 <td>Advanced Parameters(Minimum Priority)</td><td>$priority_user</td>
                             </tr>
                             <tr>
                                 <td>Number of Output microRNAs</td><td>$number_of_output<a href=\"$session_output_url\"><b>   download Result</b></a><br><img alt="expand" src='http://bio1.uni.lu:8081/mirna/database/images/plus.gif' id="expand" class="toclick"> Expand All <img alt="collapse" src='http://bio1.uni.lu:8081/mirna/database/images/minus.gif' id="collapse" class="toclick">Collapse All
                                 </td>
                             </tr>                             
                         </table><!--#factsheet-->
<br>
<ul class="accordion">
HEREDOCEND
        print $heredoc;
        ###################################
        #print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>No. of matching refseq transcript IDs : $size</b></font><br></td>\n";
    }#else
#    print "</tr>\n";
    #print the link for output downloading
#    print "<tr>\n";
#    print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><a href=\"$session_output_url\"><b>Result tsv file downloading</b></a></font></td>\n";
#    print "</tr>\n";
#			print "<tr>\n";
#				print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Legend</b></font></td>\n";
#				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><i>: The following table is sortable</i><br></font></td>\n";
#			print "</tr>\n";
    my $numdisplay = 30;
    $position++;
    $position--;

    my @subSet = splice(@keys, $position, $numdisplay);
#	if($input_type eq "mirbase_name") {
#		my $call_sub_table_view = &sub_table_view(\@subSet, $session, $list_name, $org, \%table_hash);#table hash contains the tablehash{major_id}{secondary_id}{'priority'}#{'detail'}
#	}
    if($input_type =~ "mirbase") {
        my $call_sub_table_view = &sub_table_view_new(\@subSet, $session, $list_name, $org, \%result_hash);#table hash contains the tablehash{major_id}{secondary_id}{'priority'}#{'detail'}
    }
    else {
#		my $call_sub_table_view = &sub_table_view_gene_centric(\@subSet, $session, $list_name, $org, \%result_hash);

        my $call_sub_table_view = &sub_table_view_gene_centric_new(\@subSet, $session, $list_name, $org, \%result_hash);

    }
    # my $total = $size;
#   my ($nextstring,$prevstring,$firststring,$laststring,$startno,$endno) = &BuildNextPrevLinksForKeywordSearchSort("true", $total, $numdisplay, $position, $section, $session,$input_type, $sort_by_field_name, $asc_or_desc);
    # print "<br>\n";
    #  print "<table cellspacing='0' border='0' align='right'>\n";
    #  print "<tr>\n";
    # print "<td align=\"right\"><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>&nbsp;&nbsp;&nbsp;&nbsp;$firststring</b></font></td>\n";
    # print "<td align=\"right\"><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>&nbsp;&nbsp;&nbsp;&nbsp;$prevstring</b></font></td>\n";
    # print "<td align=\"right\"><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>&nbsp;&nbsp;&nbsp;&nbsp;$nextstring</b></font></td>\n";
    #print "<td align=\"right\"><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>&nbsp;&nbsp;&nbsp;&nbsp;$laststring</b></font></td>\n";
    # print "</tr>\n";
    # print "</tbody>\n";
    #print "</table>\n";
    ###############################
                $heredoc = <<'HEREDOCEND';
        </ul>
                       </div><!--id pagecontent-->
                </div><!--main-->

            <footer>
        		<p> If you have any feedback/suggestions or bugs please contact <a href="mailto:jiali.wang@uni.lu?subject=systecEnqury" style="color:white">jiali.wang@uni.lu</a></p>
        	</footer>
         
        </div><!--page-->
HEREDOCEND
                print $heredoc;
    ###############################

## srk srk srk
} # sub table_view

sub sub_table_view_new {
    my ($keys, $session, $list_name, $org, $result_hash) = @_;
    my %result_hash=%$result_hash;
    my  %table_hash=%{$result_hash->{'table_hash'}};
    my %priority_hash=%{$result_hash->{'priority_hash'}};
    my %mirnaname_hash=%{$result_hash->{'mirnaname_hash'}};
    #print keys %mirnaname_hash;#
    #while(my($key,$value)= each %mirnaname_hash){#
    #    print "$key:$value<br>";#
    # };#
    my @fields=@{$result_hash->{'column_names'}};#the fields for all the dbs covered
    #print @fields;#testing 
    my @keys = @$keys;#the keys of miRNAs spliced subsets

    my $imgNo = 0;

    my $i = 0;
    my $z = 0;
    foreach my $mirna_name (@keys) {
        $z++;
        my %sorted_target_hash = %{$priority_hash{$mirna_name}};
        my $target_details = "";
        foreach my $transcript_id (sort {$sorted_target_hash{$b}<=>$sorted_target_hash{$a}} keys %sorted_target_hash) {

            $target_details .= "<tr>\n";
            $target_details .= "<td class=\"bigcell\"><a class=biocompendium href=\"http://www.ncbi.nlm.nih.gov/nuccore/$transcript_id\">$transcript_id</a></td>\n";
            $target_details .= "<td class=\"smallCell\">$priority_hash{$mirna_name}{$transcript_id}</td>\n";

            foreach my $current_stat (@{$table_hash{$mirna_name}{$transcript_id}}){
                $target_details .= "<td class=\"smallCell\">$current_stat</td>\n";
            }
            
            $target_details .= "</tr>\n";
        } # foreach my $transcript_id (sort {$sorted_target_hash{$a}<=>$sorted_target_hash{$b}} keys %sorted_target_hash) {
        # print "<tbody>";
        # print "<tr>\n";
        my $toggle = "target" . $mirna_name;#for property of label
        #$imgNo++;
#http://www.mirbase.org/cgi-bin/mirna_entry.pl?acc=MI0000651
        my $mirna_namefam =$mirnaname_hash{$mirna_name};
        print "<li><label for=\'$toggle\' class=\"toclick\">#miRNA: <a class=biocompendium href=\"http://www.mirbase.org/cgi-bin/mirna_entry.pl?acc=$mirna_name\">$mirna_namefam</a></label>\n";
        print "<input type=\'checkbox\' name=\'a\' id=\'$toggle\' class=\'mycheckbox\'><label></label>\n";
        print "<div class=\'content\'>\n";
        print "<div id=\"tableContainer\" class=\"tableContainer\">\n";
        print "<table class=\"sortable\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">\n";
        print "<thead class=\"fixedHeader\">\n";
        ####starting of thead content
        print "<tr>\n";
        print "<th class=\"bigcell\"><div class=\"verticalText\">Refseq Transcript ID</div></th>\n";
        print "<th class=\"smallCell\"><div id=\'smallCell\' class=\"verticalText\">Priority</div></th>\n";
        foreach my $current_field (@fields){
            if ($current_field=~'tarbase'){
                print  "<th class=\"smallCell\" bgcolor=\"#000000\"><div id=\'smallCell\' class=\"verticalText\"> $tool_mappings{$current_field}</div></th>\n";
            }else{
                print  "<th class=\"smallCell\"><div id=\'smallCell\'class=\"verticalText\">$tool_mappings{$current_field}</div></th>\n";}  
        }
        # print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Priority </b></font></td>\n";
        print "</tr>\n";
        print "</thead>\n";
        print "<tbody class=\'scrollContent\'>\n";
        print "$target_details";

        print "</tbody>\n";
        print "</table>\n";
        print "</div>\n";
        print "</div>\n";
        print "<br>\n";
        print "</li>\n";    
    } # foreach my $cluster_id (@cluster_ids) {

}# sub sub_table_view_new {

sub sub_table_view_gene_centric_new {
    my ($keys, $session, $list_name, $org, $result_hash) = @_;
    my %result_hash=%$result_hash;
    my  %table_hash=%{$result_hash->{'table_hash'}};
    my %priority_hash=%{$result_hash->{'priority_hash'}};
    my %mirnaname_hash=%{$result_hash->{'mirnaname_hash'}};
    my @fields=@{$result_hash->{'column_names'}};#the fields for all the dbs covered
    my @keys = @$keys;#the keys of miRNAs spliced subsets



    my $i = 0;
    my $z = 0;
    foreach my $refseq_name (@keys) {
        $z++;
        my %sorted_target_hash = %{$priority_hash{$refseq_name}};
        my $target_details = "";

        foreach my $mirna_name (sort {$sorted_target_hash{$b}<=>$sorted_target_hash{$a}} keys %sorted_target_hash) {
            ####################################
            $target_details .= "<tr>\n";
            $target_details .= "<td class=\"bigcell\"><a class=biocompendium href=\"http://www.mirbase.org/cgi-bin/mirna_entry.pl?acc=$mirna_name\">$mirnaname_hash{$mirna_name}</a></td>\n";
            $target_details .= "<td class=\"smallCell\">$priority_hash{$refseq_name}{$mirna_name}</td>\n";

            foreach my $current_stat (@{$table_hash{$refseq_name}{$mirna_name}}){
                $target_details .= "<td class=\"smallCell\">$current_stat</td>\n";
            }
            
            $target_details .= "</tr>\n";
            ######################################     
           
        } # foreach my $transcript_id (sort {$sorted_target_hash{$a}<=>$sorted_target_hash{$b}} keys %sorted_target_hash) {

        my $toggle = "target" . $refseq_name;
        #$imgNo++;
        #####################################
        print "<li><label for=\'$toggle\' class=\"toclick\">#Refseq transcript ID: <a class=biocompendium href=\"http://www.ncbi.nlm.nih.gov/nuccore/$refseq_name\">$refseq_name</a></label>\n";
        print "<input type=\'checkbox\' name=\'a\' id=\'$toggle\' class=\'mycheckbox\'><label></label>\n";
        print "<div class=\'content\'>\n";
        print "<div id=\"tableContainer\" class=\"tableContainer\">\n";
        print "<table class=\"sortable\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">\n";
        print "<thead class=\"fixedHeader\">\n";
        ####starting of thead content
        print "<tr>\n";
        print "<th class=\"bigcell\"><div class=\"verticalText\">microRNA name</div></th>\n";
        print "<th class=\"smallCell\"><div id=\'smallCell\' class=\"verticalText\">Priority</div></th>\n";
        foreach my $current_field (@fields){
            if ($current_field=~'tarbase'){
                print  "<th class=\"smallCell\" bgcolor=\"#000000\"><div id=\'smallCell\' class=\"verticalText\">$tool_mappings{$current_field}</div></th>\n";
            }else{
                print  "<th class=\"smallCell\"><div id=\'smallCell\'class=\"verticalText\">$tool_mappings{$current_field}</div></th>\n";}  
        }
       
        print "</tr>\n";
        print "</thead>\n";
        print "<tbody class=\'scrollContent\'>\n";
        print "$target_details";

        print "</tbody>\n";
        print "</table>\n";
        print "</div>\n";
        print "</div>\n";
        print "<br>\n";
        print "</li>\n";    
        #####################################

    } # foreach my $cluster_id (@cluster_ids) {

}# sub_table_view_gene_centric_new {




sub BuildNextPrevLinksForKeywordSearchSort {
    my ($blankon,$total,$numdisplay,$position, $section, $session, $input_type, $sort_by_field_name, $asc_or_desc) = @_;
    my ($startno,$endno,$prevstring,$nextstring,$firststring,$laststring);

    return unless ($total || $blankon);
    $numdisplay=15 unless $numdisplay;

    # calculations need to be based on total found not our display total
    if ($total > $numdisplay) {
        $startno = $position+1;
        $endno = $startno + ($numdisplay - 1);
        $endno = $total if ($endno > $total);
    }
    else {
        # when we have less than the number of rows passed in
        $startno = 1;
        $endno = $total;
    }

    if ($position>=$numdisplay) {
        my $newquerystring;
        my $prevstart = $position - $numdisplay;

        my $prevlink = &EditQueryStringForKeywordSearchSort($prevstart, $section, $session, $input_type, $sort_by_field_name, $asc_or_desc);
        $prevstring="<a href=\"$prevlink\">\< Previous </a>";

        my $firstlink = &EditQueryStringForKeywordSearchSort(0, $section, $session, $input_type, $sort_by_field_name, $asc_or_desc);
        $firststring="<a href=\"$firstlink\">\<\< First </a>";
    }
    else {
        $prevstring="\< Previous " if ($blankon);
        $firststring="\<\< First " if ($blankon);
    }

    if ($endno<$total){
        my $nextstart = $position + $numdisplay;
        my $how_many_left = $total - $nextstart;

        if ($how_many_left > $numdisplay) {
            $how_many_left = $numdisplay;
        }
        my $nextlink = &EditQueryStringForKeywordSearchSort($nextstart, $section, $session, $input_type, $sort_by_field_name, $asc_or_desc);
        $nextstring="<a href=\"$nextlink\">Next \> ";

        my $lastpagenum = ($total % $numdisplay);
        my $laststart = $total - $lastpagenum;

        my $lastlink = &EditQueryStringForKeywordSearchSort($laststart, $section, $session, $input_type, $sort_by_field_name, $asc_or_desc);
        $laststring="<a href=\"$lastlink\">Last \>\> </a>";
    }
    else {
        $nextstring="Next \>" if ($blankon);
        $laststring="Last \>\>" if ($blankon);
    }

    return ($nextstring,$prevstring,$firststring,$laststring,$startno,$endno);
} # sub BuildNextPrevLinksForKeywordSearchSort {

sub EditQueryStringForKeywordSearchSort {
    my ($pos, $section, $session, $input_type, $sort_by_field_name, $asc_or_desc) = @_;
    my $link = "$URL_cgi?section=$section&pos=$pos&session=$session&Category1=$input_type&sort=$sort_by_field_name&ad=$asc_or_desc";
    $link;
} # sub EditQueryStringForKeywordSearchSort {



sub BuildNextPrevLinksForKeywordSearch {
    my ($blankon,$total,$numdisplay,$position, $section, $org, $session, $list_name) = @_;
    my ($startno,$endno,$prevstring,$nextstring,$firststring,$laststring);

    return unless ($total || $blankon);
    $numdisplay=15 unless $numdisplay;

    # calculations need to be based on total found not our display total
    if ($total > $numdisplay) {
        $startno = $position+1;
        $endno = $startno + ($numdisplay - 1);
        $endno = $total if ($endno > $total);
    }
    else {
        # when we have less than the number of rows passed in
        $startno = 1;
        $endno = $total;
    }

    if ($position>=$numdisplay) {
        my $newquerystring;
        my $prevstart = $position - $numdisplay;

        my $prevlink = &EditQueryStringForKeywordSearch($prevstart, $section, $org, $session, $list_name);
        $prevstring="<a href=\"$prevlink\">\< Previous </a>";

        my $firstlink = &EditQueryStringForKeywordSearch(0, $section, $org, $session, $list_name);
        $firststring="<a href=\"$firstlink\">\<\< First </a>";
    }
    else {
        $prevstring="\< Previous " if ($blankon);
        $firststring="\<\< First " if ($blankon);
    }

    if ($endno<$total){
        my $nextstart = $position + $numdisplay;
        my $how_many_left = $total - $nextstart;

        if ($how_many_left > $numdisplay) {
            $how_many_left = $numdisplay;
        }
        my $nextlink = &EditQueryStringForKeywordSearch($nextstart, $section, $org, $session, $list_name);
        $nextstring="<a href=\"$nextlink\">Next \> ";

        my $lastpagenum = ($total % $numdisplay);
        my $laststart = $total - $lastpagenum;

        my $lastlink = &EditQueryStringForKeywordSearch($laststart, $section, $org, $session, $list_name);
        $laststring="<a href=\"$lastlink\">Last \>\> </a>";
    }
    else {
        $nextstring="Next \>" if ($blankon);
        $laststring="Last \>\>" if ($blankon);
    }

    return ($nextstring,$prevstring,$firststring,$laststring,$startno,$endno);
} # sub BuildNextPrevLinksForKeywordSearch {

sub EditQueryStringForKeywordSearch {
    my ($pos, $section, $org, $session, $list_name) = @_;
    my $link = "$URL_cgi?section=$section&pos=$pos&org=$org&session=$session&list=$list_name";
    $link;
} # sub EditQueryStringForKeywordSearchSort {


sub nonRedundantList{
    my $val = shift;
    my @val=@$val;
    my %cpt;
    foreach (@val){
        $cpt{$_}++;
    }
    return keys %cpt;
} # sub redundantList{

sub getCombinations {
    my ($size, $i) = @_;
    my @n = (0 .. ($size-1));
#print "array : @n\n";
    my %allCombo = ();
    my @allComboKeys = ();
#	for (my $i=$size; $i>=2; $i--) {
    my $combinat = Math::Combinatorics->new(count => $i,
        data => [@n],
    );

    while(my @combo = $combinat->next_combination){
        @combo = sort @combo;
        my $keyStr = '';
        foreach my $m (@combo) {$keyStr = $keyStr .+ $m .+ ';';}
        chop($keyStr);
#print "keyStr : $keyStr\n";
        push @allComboKeys, $keyStr;
        $allCombo{$keyStr} =  \@combo;
#print join(',', @combo)."\n";
} # while(my @combo = $combinat->next_combination){
#	} # for (my $i=$size; $i>=2; $i--) {
#	my %result =  (allCombo => \%allCombo, allComboKeys => \@allComboKeys);
#	return \%result;
return @allComboKeys;
} # sub getCombinations {

sub create_table {
    my ($table_name, $gene_list) = @_;
    my $create_table_string = "";

    $create_table_string = "DROP TABLE IF EXISTS `$table_name`;\n";
    $create_table_string .= "CREATE TABLE `$table_name`(\n";
    $create_table_string .= "`gene` varchar(40) default NULL,\n";
    $create_table_string .= "PRIMARY KEY  (`gene`),\n";
    $create_table_string .= "UNIQUE KEY `gene` (`gene`)\n";
    $create_table_string .= ")ENGINE=MyISAM DEFAULT CHARSET=latin1;\n\n";
    $create_table_string .= "LOCK TABLES `$table_name` WRITE;\n";
    $create_table_string .= "INSERT INTO `$table_name` VALUES ";

    my @gene_list = &nonRedundantList($gene_list);
    while (@gene_list) {
        my $gene = shift @gene_list;
        $create_table_string .= "('$gene'),";
    } # while (@gene_list) { 
    chop($create_table_string);
    $create_table_string .= ";\nUNLOCK TABLES;\n\n"; 

    return $create_table_string;
} # sub create_table {

sub min {
    my ($a, $b) = @_;
    return $a<$b? $a : $b;
}
