#!/usr/bin/perl -w

#################################################################
## Developed by Venkata P. Satagopam venkata.satagopam@embl.de##
#               Jiali Wang jialimwang@gmail.com                ##
## Disclaimer: Copy rights reserved by EMBL, please contact    ## 
## Venkata Satagopam prior to reuse any part of this code      ##
#################################################################

use strict;
use lib "/home/database/projects/gist/systec/modules";
use lib "/home/database/perl5/lib/perl5";
use IdMapper;
use DbmiRNA;
use Math::Combinatorics;
use List::Compare;
use Data::Dumper;
use JSON;
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
my $pvalue = $q->("p_value");#boolean to decided if pvalue needed
my $mhd = $q->("MHD");#boolean to decide if pvalue is needed
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
    &alert;
}else{
    %toolselection = map {$_=>1} @toolselection;
}#check if it is empty #0110
if(!$pvalue){
    $pvalue = 1;
}
if(!$mhd){
    $mhd =1;
}
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
    -meta=> {keywords=>'systec microRNA target prediction jiali.wang@uni.lu'},
    -style=>{-src=>['http://bio1.uni.lu:8081/mirna/database/style/systecnew.css','http://code.jquery.com/ui/1.11.3/themes/smoothness/jquery-ui.css','http://bio1.uni.lu:8081/mirna/database/style/horizBarChart.css','http://bio1.uni.lu:8081/mirna/database/style/styleChart.css']},
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
            -src=>'http://bio1.uni.lu:8081/mirna/database/javascript/sorttable.js'},
        {-language=>'JAVASCRIPT',
            -src=>'http://http://code.jquery.com/ui/1.11.3/jquery-ui.js'},
       
        {-language=>'JAVASCRIPT',
            -src=>'http://bio1.uni.lu:8081/mirna/database/javascript/horizBarChart.js'}
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
my $tax_id= $tax_mappings{$org};

my %org_mappings = (
    'human' => 'Homo_sapiens',
    'mouse' => 'Mus_musculus',
    'yeast' => 'Saccharomyces_cerevisiae',
); 		     
#important ---toolmapping
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
&table_view(0, $session, $input_type, 'mirna_name', 'desc',$org,$session_dir,\@gene_list);#position, $session, $input_type,$sort_by_field_name(by default sort by mirna_name),$asc or desc
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
  
    my $section="biodb";
    my $query_db;#
    ##set up organism
    if($org eq 'human'){$query_db = "mirna_human_strict";}#
    if($org eq 'mouse'){$query_db= "mirna_mouse";}#not realized yet

    my $result_hash = undef;
    my %result_hash;
    my %table_hash;

    my @input_list= @{$gene_list_ref};#added
    my $input_string = "";
    my $input_nr= scalar(@input_list);#added
    if($input_type eq "mirbase_name"||$input_type eq "mirbase_accession") {
        $result_hash = &DbmiRNA::GetMirTableViewInfo($input_type, $asc_or_desc, $session, $list_name,$query_db,$session_dir,\%toolselection,$priority_user,\@tissuefilter);#field_name,asse or desc, $temp_database,$tmp_table,$query_database
        #%result_hash=%$result_hash;
        # %table_hash=%{$result_hash->{'mirna_hash'}};
    }
    else {
        $result_hash = &DbmiRNA::GetTargetTableViewInfo($input_type, $asc_or_desc, $session, $list_name,$query_db,$session_dir,\%toolselection,$priority_user,\@tissuefilter);#pass the tool selection to file
        $input_string =join ("__", @input_list);
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

    ################## if input is miRNA ################
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
<!--#button_list to sent out links-->   
<TABLE  id="button_list">
<TR >
    <TD ><input id="selectall" type="checkbox"  value="checkAll" />Check/Uncheck all &nbsp;&nbsp;</TD> 
    <TD ><input type="button" value="Biocompendium" id="biocompendium_L" />&nbsp;&nbsp;&nbsp;&nbsp; </TD>
    <TD ><input type="button" value="KEGG Enrichment" id="kegg_L" />&nbsp;&nbsp;&nbsp;&nbsp; </TD>
    <TD ><input type="button" value="Gene Ontology Enrichment" id="go_L" />&nbsp;&nbsp;&nbsp;&nbsp; </TD>
</TR>
        
</TABLE>
<!--#END——button list to sent out list-->
<ul class="accordion">
HEREDOCEND
         print $heredoc;
        ################################################
        #print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>No. of miRNAs : $size</b></font><br></td>\n";
    }
    else {
        ###################################refseq input#######
                $heredoc = <<"HEREDOCEND";
                                     <tr>
                                 <td>Number of Input mRNA</td><td>$input_nr</td>
                             </tr>
                             <tr>
                                 <td>Number of Analysed mRNA</td><td>$size &nbsp;&nbsp;<a href=\"http://biocompendium.embl.de/cgi-bin/biocompendium.cgi?section=upload_gene_lists_tamahud&background=whole_genome&org=$org&gene_list1=$org%0Agene_list_1%0Arefseq%0A$input_string\">Input Summary</a> &nbsp;</td>
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
<!--#button_list to sent out links-->   
<TABLE  id="button_list">
<TR >
    <TD ><input id="selectall" type="checkbox"  value="checkAll" />Check/Uncheck all &nbsp;&nbsp;</TD> 
    <TD ><input type="button" value="Biocompendium" id="biocompendium_L" />&nbsp;&nbsp;&nbsp;&nbsp; </TD>
    <TD ><input type="button" value="KEGG Enrichment" id="kegg_L" />&nbsp;&nbsp;&nbsp;&nbsp; </TD>
    <TD ><input type="button" value="Gene Ontology Enrichment" id="go_L" />&nbsp;&nbsp;&nbsp;&nbsp; </TD>
</TR>
        
</TABLE>
<!--#END——button list to sent out list-->
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
    # print "<br>\n";
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
#produce miRNA centric table
sub sub_table_view_new {
    my ($keys, $session, $list_name, $org, $result_hash) = @_;
    my %result_hash=%$result_hash;
    my  %table_hash=%{$result_hash->{'table_hash'}};
    my %priority_hash=%{$result_hash->{'priority_hash'}};
    my %mirnaname_hash=%{$result_hash->{'mirnaname_hash'}};
    # my %genename_hash=%{$result_hash->{'genename_hash'}};
     my %genename_hash=%{IdMapper::refseq_get_symbol($org,$result_hash->{'genename_array'}) };
    my %pvalue_hash;
    my %mhd_hash;
    if($pvalue) {%pvalue_hash=%{$result_hash->{'priority_bay_hash'}};}#changed
    if($mhd) {%mhd_hash=%{$result_hash->{'priority_weight'}};}#changed
    
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
            my $pvalue_final =1-$pvalue_hash{$refseq_name}{$mirna_name};
            $target_details .= "<tr>\n";
            $target_details .= "<td class=\"smallCell\"><input type=\"checkbox\" class=\"checkbox1\" name=\"chb\" value=\"$transcript_id\"/></td><td class=\"bigcell\"><a class=biocompendium href=\"http://www.ncbi.nlm.nih.gov/nuccore/$transcript_id\">$transcript_id</a></td>\n";#changed, for adding the checkbox for each refseq ID
            $target_details .= "<td class=\"bigcell\"><a class=biocompendium href=\"http://www.ihop-net.org/UniPub/iHOP/?search=$genename_hash{$transcript_id}&field=all&ncbi_tax_id=$tax_id\">$genename_hash{$transcript_id}</a></td>\n";#add gene name for each column
            $target_details .= "<td class=\"smallCell\">$priority_hash{$mirna_name}{$transcript_id}</td>\n";
            if($pvalue){$target_details .= "<td class=\"bigCell\">$pvalue_final</td>\n";}#changed
            if ($mhd){$target_details .= "<td class=\"bigCell\">$mhd_hash{$mirna_name}{$transcript_id}</td>\n";}#changed
                
            foreach my $current_stat (@{$table_hash{$mirna_name}{$transcript_id}}){
                $target_details .= "<td class=\"smallCell\">$current_stat</td>\n";
            }
            
            $target_details .= "</tr>\n";
        } # foreach my $transcript_id (sort {$sorted_target_hash{$a}<=>$sorted_target_hash{$b}} keys %sorted_target_hash) {
        # print "<tbody>";
        # print "<tr>\n";
        my $toggle = "target".$mirna_name;#for property of label
        #$imgNo++;

        my $mirna_namefam =$mirnaname_hash{$mirna_name};
        print "<li><label for=\'$toggle\' class=\"toclick\">#miRNA: <a class=biocompendium href=\"http://www.mirbase.org/cgi-bin/mirna_entry.pl?acc=$mirna_name\">$mirna_namefam</a></label>\n";
        print "<input type=\'checkbox\' name=\'a\' id=\'$toggle\' class=\'mycheckbox\'><label></label>\n";
        print "<div class=\'content\'>\n";
        print "<div id=\"tableContainer\" class=\"tableContainer\">\n";
        print "<table class=\"sortable\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">\n";
        print "<thead class=\"fixedHeader\">\n";
        ####starting of thead content
        print "<tr>\n";
        print "<th class=\"smallCell\"><div id=\"smallcell\"  class=\"verticalText\">#</div></th>\n";# changed, for adding a column to included the check box
        print "<th class=\"bigcell\"><div  class=\"verticalText\">Refseq Transcript ID</div></th>\n";
        print "<th class=\"bigcell\"><div  class=\"verticalText\">Gene Name</div></th>\n";
        print "<th class=\"smallCell\"><div id=\"smallcell\"  class=\"verticalText\">Priority</div></th>\n";
       if($pvalue){ print "<th class=\"bigCell\"><div class=\"verticalText\">P-value</div></th>\n";}#changed
       if($mhd) {print "<th class=\"bigCell\"><div class=\"verticalText\">MHD</div></th>\n";}#changed
        foreach my $current_field (@fields){
            if ($current_field=~'tarbase|starbase|mirRecord'){#changed
                print  "<th class=\"smallCell\" ><div id=\'smallCell\' class=\"verticalText_evi\"> $tool_mappings{$current_field}</div></th>\n";#changed adding highlight to evidence
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
    } # foreach my $cluster_id (@cluster_ids) {

}# sub sub_table_view_new {

sub sub_table_view_gene_centric_new {
    my ($keys, $session, $list_name, $org, $result_hash) = @_;
    my %result_hash=%$result_hash;
    my %table_hash=%{$result_hash->{'table_hash'}};
    my %priority_hash=%{$result_hash->{'priority_hash'}};
    my %mirnaname_hash=%{$result_hash->{'mirnaname_hash'}};
        # my %genename_hash=%{$result_hash->{'genename_hash'}};
     my %genename_hash=%{IdMapper::refseq_get_symbol($org,$result_hash->{'genename_array'}) };
    my %pvalue_hash;
    my %mhd_hash;
    if($pvalue) {%pvalue_hash=%{$result_hash->{'priority_bay_hash'}};}#changed
    if($mhd) {%mhd_hash=%{$result_hash->{'priority_weight'}};}#changed
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
            my $pvalue_final =1-$pvalue_hash{$refseq_name}{$mirna_name};
            $target_details .= "<tr>\n";
            $target_details .= "<td class=\"bigcell\"><a class=biocompendium href=\"http://www.mirbase.org/cgi-bin/mirna_entry.pl?acc=$mirna_name\">$mirnaname_hash{$mirna_name}</a></td>\n";
            $target_details .= "<td class=\"smallCell\">$priority_hash{$refseq_name}{$mirna_name}</td>\n";
            if($pvalue){$target_details .= "<td class=\"bigCell\">$pvalue_final</td>\n";}#changed
            if ($mhd){$target_details .= "<td class=\"bigCell\">$mhd_hash{$refseq_name}{$mirna_name}</td>\n";}#changed
            foreach my $current_stat (@{$table_hash{$refseq_name}{$mirna_name}}){
                $target_details .= "<td class=\"smallCell\">$current_stat</td>\n";
            }
            
            $target_details .= "</tr>\n";
            ######################################     
           
        } # foreach my $transcript_id (sort {$sorted_target_hash{$a}<=>$sorted_target_hash{$b}} keys %sorted_target_hash) {

        my $toggle = "target" . $refseq_name;
        #$imgNo++;
        #####################################
        print "<li><label for=\'$toggle\' class=\"toclick\">#<input type=\"checkbox\" class=\"checkbox1\" name=\"chb\" value=\"$refseq_name\"/>Refseq transcript ID: <a class=biocompendium href=\"http://www.ncbi.nlm.nih.gov/nuccore/$refseq_name\">$refseq_name</a> :: <a class=biocompendium href=\"http://www.ihop-net.org/UniPub/iHOP/?search=$genename_hash{$transcript_id}&field=all&ncbi_tax_id=$tax_id\">$genename_hash{$transcript_id}</a></label>\n";
        print "<input type=\'checkbox\' name=\'a\' id=\'$toggle\' class=\'mycheckbox\'><label></label>\n";
        print "<div class=\'content\'>\n";
        print "<div id=\"tableContainer\" class=\"tableContainer\">\n";
        print "<table class=\"sortable\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">\n";
        print "<thead class=\"fixedHeader\">\n";
        ####starting of thead content
        print "<tr>\n";
        print "<th class=\"bigcell\"><div class=\"verticalText\">microRNA name</div></th>\n";
        print "<th class=\"smallCell\"><div id=\'smallCell\' class=\"verticalText\">Priority</div></th>\n";
       if($pvalue){ print "<th class=\"bigCell\"><div class=\"verticalText\">P-value</div></th>\n";}#changed
       if($mhd) {print "<th class=\"bigCell\"><div class=\"verticalText\">MHD</div></th>\n";}#changed
        foreach my $current_field (@fields){
            if ($current_field=~'tarbase|starbase|miRecord'){
                print  "<th class=\"smallCell\"><div id=\'smallCell\' class=\"verticalText_evi\">$tool_mappings{$current_field}</div></th>\n";
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

# this function will be used to creat a miRNA summary _sheet for miRNA

=begin  BlockComment  # BlockCommentNo_1



sub summary_sheet { 
	my ($mir_acc) = @_;
	my $banner = &get_browse_banner("");#get_browse_banner
	my $summary_sheet = 0;
	my $geneDetails = 0;
	my $gene_name_obj = 0;
    $summary_sheet = new DbHumanSummarySheet($gene);
# from summary_sheet object
	my $id = $summary_sheet->{DBID};
	my $unified_uniprot = $summary_sheet->{UniprotID};
	my $omim = $summary_sheet->{Omim};

	if ($uniprot_acc=~/-/) {
		my @temp = split("-", $uniprot_acc);
		$uniprot_acc = $temp[0];
	}
	
	
	print "<table cellpadding=\"10\" border=\"0\"  width=$table_width>\n";
		print "<tbody>";
	my $imgNo = 0;

		print "<tr>\n";
			print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b></b></font></td>\n";
			print "<td><b>Summary sheet information for given gene $gene</b><br></td>\n";
		print "</tr>\n";
		
		print "<tr>\n";
			print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Name</b></font></td>\n";
			print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$gene_name<br></fong></td>\n";
		print "</tr>\n";

		print "<tr>\n";
			print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></font></td>\n";
			print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$description<br></font></td>\n";
		print "</tr>\n";
		
#		my $validation_str = &progeria_validation($hugo_name);
#	       print "<tr>\n";
#			print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Group</b></font></td>\n";
#			print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$validation_str<br></font></td>\n";
#		print "</tr>\n";
		print "<tr>\n";
			print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Protein Information from Dasty2  DAS Client</b></font></td>\n";
#			print "<td><iframe src=\"http://schneider.embl.de/mitocheck2/das/dasty2_client_035/mitocheck2.html?q=$uniprot_acc&label=BioSapiens&t=3\" width=\"80%\" height=\"500\"></iframe><br></td>\n";
			print "<td><iframe src=\"${dasty2das_client}?q=$uniprot_acc&label=BioSapiens&t=3\" width=\"80%\" height=\"500\"></iframe><br></td>\n";
		print "</tr>\n";

		print "<tr>\n";
			print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"></font></td>\n";
			print "<td><a href=\"#\" onclick=\"return toggleAll(\'expand\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'expand\' onClick=\'changeImage(\"expand\")\'></a> <font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Expand All</b></font><a href=\"#\" onclick=\"return toggleAll(\'collapse\')\"> <img alt=\"\" src=\"/images/minus.gif\" name=\'collapse\' onClick=\'changeImage(\"collapse\")\'></a> <font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Collapse All</b></font><br></td>\n";
		print "</tr>\n";

		print "<tr>\n";
			print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Genes</b></font></td>\n";
			print "<td>";
				print "<table cellspacing='0' width=$table_width>\n";
					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_genelocation\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> Gene Location: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

					print "<tbody class=\"collapse_obj\" id=\"collapse_genelocation\">";
						print "<tr>\n";
							print "<td>";
									print "<table>";
										print "<tr><td><font face=\"Arial\" size=\"2\" color=\"#000000\">Chromosome</font></td><td><font face=\"Arial\" size=\"2\" color=\"#000000\">: $chr_name</font></td></tr>";
										print "<tr><td><font face=\"Arial\" size=\"2\" color=\"#000000\">Gene Start</font></td><td><font face=\"Arial\" size=\"2\" color=\"#000000\">: $gene_start</font></td></tr>";
										print "<tr><td><font face=\"Arial\" size=\"2\" color=\"#000000\">Gene End</font></td><td><font face=\"Arial\" size=\"2\" color=\"#000000\">: $gene_end</font></td></tr>";
#										print "<tr><td><font face=\"Arial\" size=\"2\" color=\"#000000\"><a href=\"http://www.ensembl.org/Homo_sapiens/contigview?l=$chr_name:$gene_start-$gene_end\"><i>Ensembl Contig View</i></a></font></td><td><font face=\"Arial\" size=\"2\" color=\"#000000\"></font></td></tr>";		
										print "<tr><td><font face=\"Arial\" size=\"2\" color=\"#000000\"><a href=\"http://www.ensembl.org/$ensembl_mappings{$GenomeDBID}/contigview?l=$chr_name:$gene_start-$gene_end\"><i>Ensembl Contig View</i></a></font></td><td><font face=\"Arial\" size=\"2\" color=\"#000000\"></font></td></tr>";		
									print "</table>";
							print "<br></td>\n";
						print "</tr>\n";
					print "</tbody>";

					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_genes\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> Ensembl Genes: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

					print "<tbody class=\"collapse_obj\" id=\"collapse_genes\">\n";
						print "<tr>\n";
							print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">";
								print "<a class=biocompendium href=\"http://www.ensembl.org/$ensembl_mappings{$GenomeDBID}/geneview?gene=$gene\">$gene<br>";
							print "<br></font></td>\n";
						print "</tr>\n";
					print "</tbody>";			

					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_emblgenbankids\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> EMBL: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

					my @embl_id = split("______", $embl_genbank_id);
					my $embl_id_str = "<table>";
					$embl_id_str .= "<tr><td bgcolor= #c7c7d0 width=12%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>EMBL ID</b></td><td  bgcolor= #c7c7d0>&nbsp;&nbsp;</td><td  bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></td></tr>";
					foreach my $e (@embl_id) {
						my ($embl_id, $embl_des_pk) = split("____", $e);
						my ($embl_des, $embl_pk) = split("__", $embl_des_pk);
# http://srs.ebi.ac.uk/srsbin/cgi-bin/wgetz?-e+[EMBL:AB020317]+-newId
# http://www.ebi.ac.uk/cgi-bin/emblfetch?style=html&id=AJ297549
						$embl_id_str .= "<tr><td><a class=biocompendium href=\"http://www.ebi.ac.uk/cgi-bin/emblfetch?style=html&id=$embl_id\">$embl_id</td><td>&nbsp;&nbsp;</td><td>$embl_des</td></tr> ";
					} #foreach my $e (@embl_id) {
					$embl_id_str .= "</table>";
					print "<tbody class=\"collapse_obj\" id=\"collapse_emblgenbankids\">\n";
						print "<tr>\n";
							print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">";
								print "$embl_id_str<br>";
							print "</font></td>\n";
						print "</tr>\n";
					print "</tbody>";

					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_entrezgeneids\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> EntrezGene: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

					my @entrezgene_id = split("______", $entrezgene_id);
					my $entrezgene_id_str = "<table>";
					$entrezgene_id_str .= "<tr><td bgcolor= #c7c7d0 width=12%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>ID</b></td><td  bgcolor= #c7c7d0>&nbsp;&nbsp;</td><td  bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></td></tr>";
					foreach my $e (@entrezgene_id) {
						my ($id, $des_pk) = split("____", $e);
						my ($des, $pk) = split("__", $des_pk);
# http://view.ncbi.nlm.nih.gov/gene/1
						$entrezgene_id_str .= "<tr><td><a class=biocompendium href=\"http://view.ncbi.nlm.nih.gov/gene/$pk\">$id</td><td>&nbsp;&nbsp;</td><td>$des</td></tr>";
					} #foreach my $e (@entrezgene_id) {
					$entrezgene_id_str .= "</table>";
					print "<tbody class=\"collapse_obj\" id=\"collapse_entrezgeneids\">\n";
						print "<tr>\n";
							print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">";
								print "$entrezgene_id_str<br>";
							print "</font></td>\n";
						print "</tr>\n";
					print "</tbody>";

					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_refseq_dna_ids\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> RefSeq DNA: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

					my @refseq_dna_id = split("______", $refseq_dna_id);
					my $refseq_dna_id_str = "<table>";
					$refseq_dna_id_str .= "<tr><td bgcolor= #c7c7d0 width=10%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>ID</b></td><td  bgcolor= #c7c7d0>&nbsp;&nbsp;</td><td  bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></td></tr>";	
					foreach my $e (@refseq_dna_id) {
						if ($e) {
							my ($id, $des_pk) = split("____", $e);
							my ($des, $pk) = split("__", $des_pk);
# http://www.ncbi.nlm.nih.gov/nucleotide/NM_130786
							$refseq_dna_id_str .= "<tr><td><a class=biocompendium href=\"http://www.ncbi.nlm.nih.gov/nucleotide/$pk\">$pk</td><td>&nbsp;&nbsp;</td><td>$des</td></tr>";
						}
					} #foreach my $e (@refseq_dna_id) {
					$refseq_dna_id_str .= "</table>";
					print "<tbody class=\"collapse_obj\" id=\"collapse_refseq_dna_ids\">\n";
						print "<tr>\n";
							print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">";
								print "$refseq_dna_id_str<br>";
							print "</font></td>\n";
						print "</tr>\n";
					print "</tbody>";

					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_unigeneids\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> UniGene: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";
					my @unigene_id = split("______", $unigene_id); 
					my $unigene_id_str = "<table>";
					$unigene_id_str .= "<tr><td bgcolor= #c7c7d0 width=10%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>ID</b></td><td  bgcolor= #c7c7d0>&nbsp;&nbsp;</td><td  bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></td></tr>";
					foreach my $u (@unigene_id) {
						my ($id, $des_pk) = split("____", $u);
						my ($des, $pk) = split("__", $des_pk);
# http://srs.ebi.ac.uk/srsbin/cgi-bin/wgetz?-e+[EMBL:AB020317]+-newId
# http://srs.ebi.ac.uk/srsbin/cgi-bin/wgetz?-id+1UF7O1_bfnZ+-e+[UNIGENE:%27Hs.489786%27]
						$unigene_id_str .= "<tr><td><a class=biocompendium href=\"http://srs.ebi.ac.uk/srsbin/cgi-bin/wgetz?-e+\[UNIGENE:$id\]+-newId\">$id</td><td>&nbsp;&nbsp;</td><td>$des</td></tr>";
					} #foreach my $e (@unigene_id) {
					$unigene_id_str .= "</table>";
					print "<tbody class=\"collapse_obj\" id=\"collapse_unigeneids\">\n";
						print "<tr>\n";
							print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">";
								print "$unigene_id_str<br>";
							print "</font></td>\n";
						print "</tr>\n";
					print "</tbody>";
				print "</table>\n";
			print "</td>\n";
		print "</tr>\n";

		print "<tr>\n";
			print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Proteins</b></font></td>\n";
			print "<td>";
				print "<table cellspacing='0' width=$table_width>\n";
					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_proteins\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> Ensembl Proteins: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

					my @protein = split(";", $protein);
					my $protein_str = "";
					foreach my $p (@protein) {
						$protein_str .= "<a class=biocompendium href=\"http://www.ensembl.org/$ensembl_mappings{$GenomeDBID}/protview?peptide=$p\">$p</a>; ";
					} #foreach my $p (@protein) {
					chop($protein_str);
					chop($protein_str);
					print "<tbody class=\"collapse_obj\" id=\"collapse_proteins\">\n";
						print "<tr>\n";
							print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">";
								print "$protein_str<br>";
							print "<br></font></td>\n";
						print "</tr>\n";
					print "</tbody>";

					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_proteinids\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> Entrez Proteins: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

					my @protein_id = split("______", $protein_id);
					my $protein_id_str = "";
					foreach my $p (@protein_id) {
						my ($id, $des_pk) = split("____", $p);
						my ($des, $pk) = split("__", $des_pk);
# http://www.ncbi.nlm.nih.gov/protein/AAA35680.1
						$protein_id_str .= "<a class=biocompendium href=\"http://www.ncbi.nlm.nih.gov/protein/$id\">$id</a>; ";
#						$protein_id_str .= "$id; ";
					} #foreach my $p (@protein_id) {
					chop($protein_id_str);
					chop($protein_id_str);
					print "<tbody class=\"collapse_obj\" id=\"collapse_proteinids\">\n";
						print "<tr>\n";
							print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">";
								print "$protein_id_str<br>";
							print "<br></font></td>\n";
						print "</tr>\n";
					print "</tbody>";


					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_refseq_peptide_ids\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> RefSeq Proteins: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

					my @refseq_peptide_id = split("______", $refseq_peptide_id);
					my $refseq_peptide_id_str = "<table>";
					$refseq_peptide_id_str .= "<tr><td bgcolor= #c7c7d0 width=10%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>ID</b></td><td  bgcolor= #c7c7d0>&nbsp;&nbsp;</td><td  bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></td></tr>";
					foreach my $r (@refseq_peptide_id) {
						my ($id, $des_pk) = split("____", $r);
						my ($des, $pk) = split("__", $des_pk);
# http://www.ncbi.nlm.nih.gov/protein/NP_570602.2
						$refseq_peptide_id_str .= "<tr><td><a class=biocompendium href=\"http://www.ncbi.nlm.nih.gov/protein/$pk\">$pk</td><td>&nbsp;&nbsp;</td><td>$des</td></tr>";
					} #foreach my $r (@refseq_peptide_id) {
					$refseq_peptide_id_str .= "</table>";
					print "<tbody class=\"collapse_obj\" id=\"collapse_refseq_peptide_ids\">\n";
						print "<tr>\n";
							print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">";
								print "$refseq_peptide_id_str<br>";
							print "</font></td>\n";
						print "</tr>\n";
					print "</tbody>";


					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_uniprot_ids\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> UniProt: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

					my @unified_uniprot = split("______", $unified_uniprot);
					my $unified_uniprot_str = "<table>";
					$unified_uniprot_str .= "<tr><td bgcolor= #c7c7d0 width=12%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>ID</b></td><td  bgcolor= #c7c7d0>&nbsp;&nbsp;</td><td  bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></td></tr>";
					foreach my $u (@unified_uniprot) {
						my ($id, $des_pk) = split("____", $u);
						my ($des, $pk) = split("__", $des_pk);
# http://www.uniprot.org/uniprot/P04637
						$unified_uniprot_str .= "<tr><td><a class=biocompendium href=\"http://www.uniprot.org/uniprot/$id\">$id</td><td>&nbsp;&nbsp;</td><td>$des</td></tr>";
					} #foreach my $u (@unified_uniprot) {
					$unified_uniprot_str .= "</table>";
					print "<tbody class=\"collapse_obj\" id=\"collapse_uniprot_ids\">\n";
						print "<tr>\n";
							print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">";
								print "$unified_uniprot_str<br>";
							print "</font></td>\n";
						print "</tr>\n";
					print "</tbody>";

				if ($org eq "human") {
### human protein atlas only for human
use DbLink;				
					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_hpa_ids\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> Human Protein Atlas: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

					my  @hpa_ids = &DbLink::GetHumanProteinAtlasIdForGene($gene, $org);
					my $hpa_id_str = "";
					foreach my $hpa_id (@hpa_ids) {
# http://www.proteinatlas.org/gene_info.php?ensembl_gene_id=ENSG00000....
						$hpa_id_str .= "<a class=biocompendium href=\"http://www.proteinatlas.org/gene_info.php?ensembl_gene_id=$gene\">$hpa_id</a>; ";
					} # foreach my $hpa_id (@hpa_ids) {
					chop($hpa_id_str);
					chop($hpa_id_str);
					print "<tbody class=\"collapse_obj\" id=\"collapse_hpa_ids\">\n";
						print "<tr>\n";
							print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">";
								print "$hpa_id_str<br>";
							print "</font></td>\n";
						print "</tr>\n";
					print "</tbody>";

### link to mitocheck only for human
					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_mitocheck_link\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> MitoCheck: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

# http://www.mitocheck.org/cgi-bin/mtc?query=ENSG00000158406
          my $mitocheck_link .= "<a class=biocompendium href=\"http://www.mitocheck.org/cgi-bin/mtc?query=$gene\">Link to MitoCheckDB</a>";
          print "<tbody class=\"collapse_obj\" id=\"collapse_mitocheck_link\">\n";
            print "<tr>\n";
              print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">";
                print "$mitocheck_link<br>";
              print "<br></font></td>\n";
            print "</tr>\n";
          print "</tbody>";
				} # if ($org eq "human") {
				print "</table>\n";
			print "</td>\n";
		print "</tr>\n";

		print "<tr>\n";
			print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Domains</b></font></td>\n";
			print "<td>";
				print "<table cellspacing='0' width=$table_width>\n";
					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_smart\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> SMART: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";
					print "<tbody class=\"collapse_obj\" id=\"collapse_smart\">\n";
						print "<tr>\n";
							print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">";
								my $graph_protein_str = join(" ", @protein);
								my $call_graph_view = &graph_view($graph_protein_str, "Smart", $org, 'summary_sheet');
							print "</font></td>\n";
						print "</tr>\n";
					print "</tbody>";

					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_interpro\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> InterPro: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

					my @interpro = split("______", $interpro);
					my $interpro_str = "<table>";
					$interpro_str .= "<tr><td bgcolor= #c7c7d0 width=10%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>ID</b></td><td  bgcolor= #c7c7d0>&nbsp;&nbsp;</td><td  bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Name</b></td></tr>";
					foreach my $i (@interpro) {
						my ($id, $des_pk) = split("____", $i);
						my ($des, $pk) = split("__", $des_pk);
						$interpro_str .= "<tr><td><a class=biocompendium href=\"http://www.ebi.ac.uk/interpro/IEntry?ac=$id\">$id</td><td>&nbsp;&nbsp;</td><td>$des</td></tr> ";
					} #foreach my $i (@interpro) {
					$interpro_str .= "</table>";
					print "<tbody class=\"collapse_obj\" id=\"collapse_interpro\">\n";
						print "<tr>\n";
							print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">";
								print "$interpro_str<br>";
							print "</font></td>\n";
						print "</tr>\n";
					print "</tbody>";

					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_pfam\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> Pfam: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

					my @pfam_id = split("______", $pfam_id);
					my $pfam_id_str = "<table>";
					$pfam_id_str .= "<tr><td bgcolor= #c7c7d0 width=10%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>ID</b></td><td  bgcolor= #c7c7d0>&nbsp;&nbsp;</td><td  bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></td></tr>";
					foreach my $p (@pfam_id) {
						my ($id, $des_pk) = split("____", $p);
						my ($des, $pk) = split("__", $des_pk);
						$pfam_id_str .= "<tr><td><a class=biocompendium href=\"http://pfam.sanger.ac.uk/family?acc=$pk\">$id</td><td>&nbsp;&nbsp;</td><td>$des</td></tr>";
					} #foreach my $p (@pfam_id) {
					$pfam_id_str .= "</table>";
					print "<tbody class=\"collapse_obj\" id=\"collapse_pfam\">\n";
						print "<tr>\n";
							print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">";
								print "$pfam_id_str<br>";
							print "</font></td>\n";
						print "</tr>\n";
					print "</tbody>";
				print "</table>\n";
			print "</td>\n";
		print "</tr>\n";

		print "<tr>\n";
			print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Structure</b></font></td>\n";
			print "<td>";
				print "<table cellspacing='0' width=$table_width>\n";
					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_pdb\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> PDB: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

					my @pdb_id = split("______", $pdb_id);
					my $pdb_id_str = "<table>";
					$pdb_id_str .= "<tr><td bgcolor= #c7c7d0 width=10%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>ID</b></td><td  bgcolor= #c7c7d0>&nbsp;&nbsp;</td><td  bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></td></tr>";
					foreach my $p (@pdb_id) {
						my ($id, $des_pk) = split("____", $p);
						my ($des, $pk) = split("__", $des_pk);
# http://www.rcsb.org/pdb/explore/explore.do?structureId=2B6H
						$pdb_id_str .= "<tr><td><a class=biocompendium href=\"http://www.rcsb.org/pdb/explore/explore.do?structureId=$id\">$id</td><td>&nbsp;&nbsp;</td><td>$des</td></tr>";
#https://titan.embl.de:8888/srs_devel/showEntryView.do?entryId=PDB:1A1U
					} #foreach my $p (@pdb_id) {
					$pdb_id_str .= "</table>";
					print "<tbody class=\"collapse_obj\" id=\"collapse_pdb\">\n";
						print "<tr>\n";
							print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">";
								print "$pdb_id_str<br>";
							print "</font></td>\n";
						print "</tr>\n";
					print "</tbody>";

					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_hssp\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> HSSP: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

					my @hssp_id = split("______", $hssp_id);
					my $hssp_id_str = "<table>";
					$hssp_id_str .= "<tr><td bgcolor= #c7c7d0 width=10%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>ID</b></td><td  bgcolor= #c7c7d0>&nbsp;&nbsp;</td><td  bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></td></tr>";
					foreach my $p (@hssp_id) {
						my ($id, $des_pk) = split("____", $p);
						my ($des, $pk) = split("__", $des_pk);
						$hssp_id_str .= "<tr><td><a class=biocompendium href=\"https://srs.embl.de/srs/showEntryView.do?query=\[HSSP-id:$id\]\">$id</td><td>&nbsp;&nbsp;</td><td>$des</td></tr>";
					} #foreach my $p (@hssp_id) {
					$hssp_id_str .= "</table>";
					print "<tbody class=\"collapse_obj\" id=\"collapse_hssp\">\n";
						print "<tr>\n";
							print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">";
								print "$hssp_id_str<br>";
							print "</font></td>\n";
						print "</tr>\n";
					print "</tbody>";

					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_pssh\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> PSSH: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

					my @pssh_id = split("______", $pssh_id);
					my $pssh_id_str = "<table>";
					$pssh_id_str .= "<tr><td bgcolor= #c7c7d0 width=10%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>ID</b></td><td  bgcolor= #c7c7d0>&nbsp;&nbsp;</td><td  bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></td></tr>";
					foreach my $p (@pssh_id) {
						my ($id, $des_pk) = split("____", $p);
						my ($des, $pk) = split("__", $des_pk);
						$pssh_id_str .= "<tr><td><a class=biocompendium href=\"https://srs.embl.de/srs/showEntryView.do?query=\[PSSH-acc:$id\]\">$id</td><td>&nbsp;&nbsp;</td><td>$des</td></tr>";
					} #foreach my $p (@pssh_id) {
					$pssh_id_str .= "</table>";
					print "<tbody class=\"collapse_obj\" id=\"collapse_pssh\">\n";
						print "<tr>\n";
							print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">";
								print "$pssh_id_str<br>";
							print "</font></td>\n";
						print "</tr>\n";
					print "</tbody>";
				print "</table>\n";
			print "</td>\n";
		print "</tr>\n";


		print "<tr>\n";
			print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Diseases</b></font></td>\n";
			print "<td>";
				print "<table cellspacing='0' width=$table_width>\n";
					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_omim\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> OMIM: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

					my @omim = split("______OMIM:", $omim);
					my $omim_str = "<table>";
					$omim_str .= "<tr><td bgcolor= #c7c7d0 width=10%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>OMIM ID</b></td><td  bgcolor= #c7c7d0>&nbsp;&nbsp;</td><td  bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Name</b></td><td  bgcolor= #c7c7d0>&nbsp;&nbsp;</td><td  bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Alt Name</b></td></tr> ";
					foreach my $o (@omim) {
						my ($o_id, $o_des, $o_altname_pk) = split("____", $o);
						$o_id =~ s/OMIM://;
						my ($o_altname, $o_pk) = split("__", $o_altname_pk);
						$omim_str .= "<tr><td><a class=biocompendium href=\"https://srs.embl.de/srs/showEntryView.do?entryId=OMIM:$o_id\">$o_id</td><td>&nbsp;&nbsp;</td><td>$o_des</td><td>&nbsp;&nbsp;</td><td>$o_altname</td></tr> ";
					} #foreach my $i (@omim) {
					$omim_str .= "</table>";
					print "<tbody class=\"collapse_obj\" id=\"collapse_omim\">\n";
						print "<tr>\n";
							print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">";
								print "$omim_str<br>";
							print "</font></td>\n";
						print "</tr>\n";
					print "</tbody>";
				print "</table>\n";
			print "</td>\n";
		print "</tr>\n";

		print "<tr>\n";
			print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Gene Ontology</b></font></td>\n";
			print "<td>";
				print "<table cellspacing='0' width=$table_width>\n";
					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_go\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> GO: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

					my @go = split("______", $go);
					my $go_str = "<table>";
					$go_str .= "<tr><td bgcolor= #c7c7d0 width=10%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>GO ID</b></td><td  bgcolor= #c7c7d0>&nbsp;&nbsp;</td><td  bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></td></tr>";
					foreach my $g (@go) {
						my ($id, $des_pk) = split("____", $g);
						my ($des, $pk) = split("__", $des_pk);
						$go_str .= "<tr><td><a class=biocompendium href=\"https://srs.embl.de/srs/showEntryView.do?entryId=GO:$id\">$id</td><td>&nbsp;&nbsp;</td><td>$des</td></tr> ";
					} #foreach my $g (@interpro) {
					$go_str .= "</table>";
					print "<tbody class=\"collapse_obj\" id=\"collapse_go\">\n";
						print "<tr>\n";
							print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">";
								print "$go_str<br>";
							print "</font></td>\n";
						print "</tr>\n";
					print "</tbody>";
				print "</table>\n";
			print "</td>\n";
		print "</tr>\n";

		print "<tr>\n";
			print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Pathway</b></font></td>\n";
			print "<td>";
				print "<table cellspacing='0' width=$table_width>\n";
					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_kegg\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> KEGG: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

					my @pathway = split("______", $pathway);
					my $pathway_str = "<table>";
					$pathway_str .= "<tr><td bgcolor= #c7c7d0 width=12%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>KEGG PATHWAY ID</b></td><td  bgcolor= #c7c7d0>&nbsp;&nbsp;</td><td  bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Name</b></td></tr>";
					foreach my $p (@pathway) {
						my ($id, $des_pk) = split("____", $p);
						my ($des, $pk) = split("__", $des_pk);
						$id =~ s/PATHWAY://;
						$pathway_str .= "<tr><td><a class=biocompendium href=\"https://srs.embl.de/srs/showEntryView.do?entryId=PATHWAY:$id\">$id</td><td>&nbsp;&nbsp;</td><td>$des</td></tr> ";
					} #foreach my $p (@interpro) {
					$pathway_str .= "</table>";
					print "<tbody class=\"collapse_obj\" id=\"collapse_kegg\">\n";
						print "<tr>\n";
							print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">";
								print "$pathway_str<br>";
							print "</font></td>\n";
						print "</tr>\n";
					print "</tbody>";

					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_panther\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> Panther: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

					my @panther = split("______", $panther);
					my $panther_str = "<table>";
					$panther_str .= "<tr><td bgcolor= #c7c7d0 width=12%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>ID</b></td><td  bgcolor= #c7c7d0>&nbsp;&nbsp;</td><td  bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></td></tr>";

					foreach my $p (@panther) {
						my ($id, $des_pk) = split("____", $p);
						my ($des, $pk) = split("__", $des_pk);
						$id =~ s/PANTHER://;
						$panther_str .= "<tr><td><a class=biocompendium href=\"http://www.pantherdb.org/pathway/pathwayList.do?searchType=basic&fieldName=all&searchAll=true&listType=8&fieldValue=$id\">$id</td><td>&nbsp;&nbsp;</td><td>$des</td></tr>";
					} #foreach my $p (@panther) {
					$panther_str .= "</table>";
					print "<tbody class=\"collapse_obj\" id=\"collapse_panther\">\n";
						print "<tr>\n";
							print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">";
								print "$panther_str<br>";
							print "</font></td>\n";
						print "</tr>\n";
					print "</tbody>";
				print "</table>\n";
			print "</td>\n";
		print "</tr>\n";


		print "<tr>\n";
			print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Chemicals</b></font></td>\n";
			print "<td>";
				print "<table cellspacing='0' width=$table_width>\n";
# drugs ...
					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_drugs\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> Drugs: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";
					
					my $chemistry = &get_chemistry($gene, $org);
					my %chemistry = %$chemistry;
					my $drugs = $chemistry{drugs};
					my %drugs = %$drugs;

					my $drug_relevance = $chemistry{drug_relevance};
					my %drug_relevance = %$drug_relevance;

					print "<tbody class=\"collapse_obj\" id=\"collapse_drugs\">\n";
						foreach my $drug (sort { $drug_relevance{$b} <=> $drug_relevance{$a} } keys %drug_relevance) {
							my $cid = $drugs{$drug}{cid};
							if($cid) {
								my $str = $drugs{$drug}{str};
								my $cid_link = $drugs{$drug}{cid_link};
						       		print "<tr>\n"; 
							  		print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$str</font></td>";      
									my $cid_image = &get_chemical_structure($cid);	
#print "+durg: $drug, cid: $cid, str: $str, cid_image: $cid_image-\n";	
						       		 	print "<td><a href=\"$cid_link\" target=\"_blank\"><img src=\"$cid_image\" border=0></a></td></tr>";
								print "</tr>\n";
							} # if($cid) {
						} # foreach my $drug (sort { $drug_relevance{$b} <=> $drug_relevance{$a} } keys %drug_relevance) {
					print "</tbody>\n";

# ligands (pdb_ligand)
					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_ligands\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> Ligands: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

					my $ligands = $chemistry{ligands};
					my %ligands = %$ligands;

					print "<tbody class=\"collapse_obj\" id=\"collapse_ligands\">\n";
						foreach my $ligand (keys %ligands) {
							my $cid = $ligands{$ligand}{cid};
							if($cid) {
								my $str = $ligands{$ligand}{str};
								my $cid_link = $ligands{$ligand}{cid_link};
						       		print "<tr>\n"; 
							  		print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$str</font></td>";      
									my $cid_image = &get_chemical_structure($cid);	
						       		 	print "<td><a href=\"$cid_link\" target=\"_blank\"><img src=\"$cid_image\" border=0></a></td></tr>";
								print "</tr>\n";
							} # if($cid) {
						} # foreach my $ligand (keys %ligands) {
					print "</tbody>\n";

# metabolities (hmdb)
					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_metabolites\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> Metabolities: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

					my $metabolites = $chemistry{metabolites};
					my %metabolites = %$metabolites;

					print "<tbody class=\"collapse_obj\" id=\"collapse_metabolities\">\n";
						foreach my $metabolite (keys %metabolites) {
							my $cid = $metabolites{$metabolite}{cid};
							if($cid) {
								my $str = $metabolites{$metabolite}{str};
								my $cid_link = $metabolites{$metabolite}{cid_link};
						       		print "<tr>\n"; 
							  		print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$str</font></td>";      
									my $cid_image = &get_chemical_structure($cid);	
						       		 	print "<td><a href=\"$cid_link\" target=\"_blank\"><img src=\"$cid_image\" border=0></a></td></tr>";
								print "</tr>\n";
							} # if($cid) {
						} # foreach my $metabolite (keys %metabolites) {
					print "</tbody>\n";

# other chemicals 
					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_other_chemicals\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> Other chemicals: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";

					my $other_chemicals = $chemistry{other_chemicals};
					my %other_chemicals = %$other_chemicals;
					my $other_chemical_relevance = $chemistry{other_chemical_relevance};
					my %other_chemical_relevance = %$other_chemical_relevance;

					print "<tbody class=\"collapse_obj\" id=\"collapse_other_chemicals\">\n";
						foreach my $other (sort { $other_chemical_relevance{$b} <=> $other_chemical_relevance{$a} } keys %other_chemical_relevance) {
							my $cid = $other_chemicals{$other}{cid};
							if($cid) {
								my $str = $other_chemicals{$other}{str};
								my $cid_link = $other_chemicals{$other}{cid_link};
						       		print "<tr>\n"; 
							  		print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$str</font></td>";      
									my $cid_image = &get_chemical_structure($cid);	
						       		 	print "<td><a href=\"$cid_link\" target=\"_blank\"><img src=\"$cid_image\" border=0></a></td></tr>";
								print "</tr>\n";
							} # if($cid) {
						} # foreach my $metabolite (keys %metabolites) {
					print "</tbody>\n";
				print "</table>\n";
			print "</td>\n";
		print "</tr>\n";

		print "<tr>\n";
			print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>P-P, P-C Interactions</b></font></td>\n";
			print "<td>";
				print "<table cellspacing='0' width=$table_width>\n";
					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
							print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_pppcinteractions\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> Protein-Protein, Protein-Chemistry Interactions: </b></font>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";
					
					my $pppci_img = "interactions/pc_" . $org . "/" . $gene . "_pc.png"; 
					my $interaction_str = "<a href=\"http://stitch.embl.de/interactions/$gene\"><img alt=\"\" src=\"/images/$pppci_img\" border='0'></a>";
					print "<tbody class=\"collapse_obj\" id=\"collapse_pppcinteractions\">\n";
						print "<tr>\n";
							print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">";
								print "$interaction_str<br>";
							print "<br></font></td>\n";
						print "</tr>\n";
					print "</tbody>";
				print "</table>\n";
			print "</td>\n";
		print "</tr>\n";

		print "<tr>\n";
			print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Orthology</b></font></td>\n";
			print "<td>";
				print "<table border=0 cellspacing='0'>\n";
					print "<tbody>";
						print "<tr>\n";
							$imgNo++;
								print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_orthology\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> Orthology Relations: </b></font></td>\n";
						print "</tr>\n";
					print "</tbody>";

					print "<tbody class=\"collapse_obj\" id=\"collapse_orthology\">\n";
						print "<tr>\n";
							print "<td>";
								print "<table border=1 cellspacing='0'>\n";
									print "<tr>\n";
										print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Gene </b></font></td>\n";
										print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Gene Description</b></font></td>\n";
										print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Organism </b></font></td>\n";
										print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Orthology type </b></font></td>\n";
										print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Orthologs </b></font></td>\n";
										print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Orthologs Description</b></font></td>\n";
					       		 		print "</tr>\n";
# srk srk 007
									my $oid = "";
									my $orthology = "";

									if ($org eq 'human') {	
										$oid = DbHumanOrthology::GetOrthologyIdForProtein($longest_protein);
										$orthology = new DbHumanOrthology($oid);
									}
									elsif ($org eq 'mouse') {
										$oid = DbMouseOrthology::GetOrthologyIdForProtein($longest_protein);
										$orthology = new DbMouseOrthology($oid);
									}
									elsif ($org eq 'yeast') {
										$oid = DbYeastOrthology::GetOrthologyIdForProtein($longest_protein);
										$orthology = new DbYeastOrthology($oid);
									}

									print "<tr>\n";
										my $GeneDBID_des = $orthology->{GeneDBID};

										my ($GeneDBID, $gene_des) = split("\\[des\\]", $GeneDBID_des);
										my ($dbid, $Gene) = split(":", $GeneDBID);
										$GenomeDBID = $orthology->{GenomeDBID};
										my $Orthologs= $orthology->{Orthologs};
										my $OrthologsDetails= $orthology->{OrthologsDetails};

										my @Ortho = split("__", $Orthologs);
										my $OrthoSize = @Ortho;
										if ($OrthoSize > 1) {
											my @OrthologsDetails = split("____", $OrthologsDetails);
											shift @OrthologsDetails;
											my $rowSpan = @OrthologsDetails;
											print "<tr><td rowspan=\"$rowSpan\"><font face=\"Arial\" size=\"2\" color=\"#000000\"><a class=biocompendium href=\"http://www.ensembl.org/$ensembl_mappings{$GenomeDBID}/geneview?gene=$Gene\">$Gene ($gene_name)</font></td>\n";
											print "<td rowspan=\"$rowSpan\"><font face=\"Arial\" size=\"2\" color=\"#000000\">$gene_des</font></td>\n";
											foreach my $od (@OrthologsDetails) {
												my ($GeneDBID_des, $orthology_type) = split("__", $od);
												my ($GeneDBID, $gene_des) = split("\\[des\\]", $GeneDBID_des);
												my ($dbid, $Gene) = split(":", $GeneDBID);
												if ($dbid =~ /^\d+$/) {
													print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><i>$ensembl_mappings{$dbid}</i></font></td>";
													print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$orthotype{$orthology_type}</font></td>";
													print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><a class=biocompendium href=\"http://www.ensembl.org/$ensembl_mappings{$dbid}/geneview?gene=$Gene\">$Gene</font></td>";
								       	 				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$gene_des</font></td></tr>";
												} # if ($dbid =~ /^\d+$/) {
											} # foreach my $od (@OrthologsDetails) {
										} # if ($OrthoSize > 1) { 
									print "</tr>\n";
								print "</table>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";
				print "</table>\n";
			print "</td>\n";
		print "</tr>\n";
print "<script type=\"text/javascript\" src=\"$URL_project/javascript/overlib.js\"></script>\n";
} # sub summary_sheet {
sub get_banner{
		print "<!--      Developed by Venkata P. Satagopam   -->\n";#print hidden information inside the page(comments)
		print "<!--	     as part of his PhD thesis		   		 -->\n";
		print "<!--									   											 -->\n";
		print "<!--		venkata.satagopam\@embl.de	       		 -->\n";
		print "<!--									   											 -->\n";d
	print "<table  cellspacing=\"0\" cellpadding=\"0\" border=\"0\" width=\"100%\">"; 
	print "<tr>";	 
	print "<td  bgcolor= #000049>"; 
	print "<table  cellspacing=\"0\" cellpadding=\"0\" border=\"0\">"; 
	print "<tr>";				 
	print "<td  rowspan=2><img src=\"/images/icon.png\" width=\"70\" height=\"70\"></td>"; 
	print "<td class=\"banner_title\">&nbsp;bioCompendium&nbsp;</td>"; 
	print "</tr>";				
	print "<tr>";				        
#	print "<td class=\"banner_subtitle\">&nbsp;&nbsp;The compendium of biological knowledge</td>"; 
	print "<td class=\"banner_subtitle\">&nbsp;&nbsp;The high-throughput experimental data analysis platform</td>"; 
	print "</tr>";				
	print "</table>";		     
	print "</td>";		
	print "<td></td>";	    
	print "</tr>";	
	print "</table>";
}
sub get_browse_banner {
	my $section = shift;
	my $home_tab = "tab";
	my $examples_tab = "tab";
	my $help_tab = "tab";
	if ($section eq "examples") {
		$examples_tab = "activetab";
	}
	elsif($section eq "help") {
		$help_tab = "activetab";
	}
	elsif($section eq "home") { 
		$home_tab = "activetab";
	}

	&get_banner();

	print "<tr>"; 
		print "<td align=\"left\">";
			print "<table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" width=\"100%\" bgcolor=\"lightgrey\">"; 
				print "<tr>"; 
					print "<td>"; 
						print "<div class=\"tabBox\" style=\"clear:both;\"></div>"; 
						print "<div class=\"tabArea\">"; 
						print "<a class=\"$home_tab\" href=\"/\">home</a>"; 
						print "<a class=\"$examples_tab\" href=\"/examples/\">examples</a>"; 
						print "<a class=\"$help_tab\" href=\"/help/\">help</a>"; 
						print "</div>"; 
					print "</td>\n"; 
					print "<td align=\"right\">\n"; 
						print "<table>\n"; 
							print "<tr>\n"; 
								print "<div><td>\n";
								print "<input name=\"search\" id=\"search\" maxlength=\"40\" alt=\"Search\" type=\"text\" size=\"40\" value=\"search...\"  onblur=\"if(this.value=='') this.value='search...';\" onfocus=\"if(this.value=='search...') this.value='';\" /><span id=\"indicator1\" style=\"display: none\"></span>   </div>\n"; 
								print "<div id=\"search_update\" style=\"display:none; border:1px solid black;background-color:white;\"></div>\n";
								print "<script type=\"text/javascript\" language=\"javascript\" charset=\"utf-8\">\n";
								print "  // <![CDATA[ \n";
      								print "new Ajax.Autocompleter('search','search_update','/cgi-bin/biocompendium_auto_select.cgi',{method:'get', minChars:1, frequency:0.1, indicator:'indicator1'});";
								print"  // ]]>\n";
								print "</script>";

								print "</td>"; 
								print "<td><input type=\"hidden\" name=\"search\"   value=\"search\" /></td>"; 
							print "</tr>"; 
						print "</table>"; 
					print "</td>"; 
				print "</tr>"; 
			print "</table>"; 
		print "</td>"; 
	print "</tr>"; 
	print "<tr>"; 
		print "<td></td>"; 
	print "</tr>"; 
print "</table>"; 
#print "<br><br><br>";
#print "<br><br><br><br>";
} #

sub transcription_factor {
	my ($position, $session, $list, $org) = @_;
	my $banner = &get_browse_banner("");
	my $human_header="BRCA1__Cebpa__CREB1__E2F1__ELK1__ELK4__ESR1__ETS1__FOXC1__FOXD1__FOXF2__FOXI1__FOXL1__GABPA__GATA2__GATA3__HLF__HNF4A__IRF1__IRF2__Lhx3__MAX__MEF2A__MIZF__MYC-MAX__Myf__MZF1_1-4__MZF1_5-13__NFIL3__NF-kappaB__NFKB1__NFYA__NHLH1__NKX3-1__NR1H2-RXRA__NR2F1__NR3C1__Pax6__PBX1__PPARG__PPARG-RXRA__REL__RELA__REST__RORA_1__RORA_2__RREB1__RXRA-VDR__SOX9__SP1__SPI1__SPIB__SRF__SRY__STAT1__TAL1-TCF3__TBP__TEAD1__TFAP2A__TLX1-NFIC__TP53__USF1__YY1__ZNF354C";
	print "<table cellpadding=\"10\" border=\"0\"  width=$table_width>\n";
		print "<tbody>";
		print "<tr>\n";
			print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></font><br></td>\n";
			print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>&nbsp;&nbsp;Transcription factor binding site profiling</b></font><br></td>\n";
		print "</tr>\n";
use DbLink;
	my $session_dir = $outPutDir . "sessions/" . $session . "/";
	my $tfbs_matrix_name = $list . "__tfbs_matrix";
	my $tfbs_matrix_file = $session_dir . $tfbs_matrix_name;
	my $tfbs_matrix2png_name = $tfbs_matrix_name . ".png";
	my $tfbs_matrix2png_file = $session_dir . $tfbs_matrix2png_name;

 
		print "<tr>\n";
			print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Graph view</b></font><br></td>\n";
			print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>&nbsp;&nbsp;<a href=\"/temp/sessions/$session/$tfbs_matrix2png_name\">Heat map</a></b></font><br></td>\n";
		print "</tr>\n";

	close FH;
	open FH,">$tfbs_matrix_file";
	my $tfbs_hash = ();
	if ($tfbs_hash) {
		print "<tr>\n";
			print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b></b></font></td>\n";
			print "<td><br>";
			print "<table cellspacing='0' border=1>\n";
		my %tfbs_hash = %$tfbs_hash;
		my @tfs = ();
		if ($org eq 'human') {
			@tfs = split /__/, $human_header;
		}
		elsif ($org eq 'mouse') {
			@tfs = split /__/, $mouse_header;
		}
# print header ......
		my $line = "Gene_name\t";
		print "<tr><td valign=\"bottom\"><font face=\"Arial\" size=\"2\" color=\"#000000\">Gene name</font></td>\n";
			foreach my $tf (@tfs) {
				$line .= "$tf\t";
				my $img_name = $tf . ".png";
				print "<td valign=\"bottom\"><img align=\"bottom\" alt=\"\" src=\"/images/tfbs/$img_name\"></td>\n";
			}
			chop($line);
			$line .= "\n";
		print "<td valign=\"bottom\"><font face=\"Arial\" size=\"2\" color=\"#000000\">&nbsp;&nbsp;Ensembl gene</font></td></tr>\n";
		foreach my $gene (keys %tfbs_hash) {
			my $name = $tfbs_hash{$gene}{name};
			my $tfbs_line = $tfbs_hash{$gene}{tfbs_line};
			my @tfbs_line = split /__/, $tfbs_line;
			$line .= "$name\t";	
				
			print "<tr><td class=biocompendium>$name</td>\n";
				my $i=0;
				foreach my $tf (@tfs) {
					$i++;
					my $value = $tfbs_line[$i-1];
					$line .= "$value\t";
					if ($value > 0) {
						print "<td class=biocompendium>&nbsp;&nbsp;<a class=biocompendium href=\"$URL_cgi?section=transcription_factor_details&org=$org&gene=$gene&gene_name=$name&tf=$tf\">$tfbs_line[$i-1]</a></td>\n";	
					} # if ($value > 0) {
					else {
						print "<td class=biocompendium>&nbsp;&nbsp;$value</td>";	
					} # else {
				} # foreach my $tf (@tfs) {
				chop($line);
				$line .= "\n";
			print "<td class=biocompendium><a class=biocompendium href=\"http://www.ensembl.org/$org_mappings{$org}/geneview?gene=$gene\">&nbsp;&nbsp;$gene</a></td></tr>\n";
		} # foreach my $gene (keys %tfbs_hash) { 
		print FH $line;
		close FH;
##tfbs matrix 2 png
		system("/usr/local/bin/matrix2png -data $tfbs_matrix_file -r -c -s -size 15:15 -map 5  -range 0:100 > $tfbs_matrix2png_file");#RScript --no-save --no-restore --verbose myRfile.R > outputFile.Rout 2>&1
	} # if ($tfbs_hash) {	
			print "</table>";	
		print "</tr>";	
	print "</td>";	
print "</tbody>";	
print "</table>";	
} # sub transcription_factor {

sub transcription_factor_details {
	my ($org, $gene, $gene_name, $tf) = @_;
	my $banner = &get_browse_banner("");
use IO::Socket::INET;
use SocketConf;
use human_tfbs_matrix_map;
	my $matrix_id = "";
	if ($org eq 'human') {
		$matrix_id = &human_tfbs_matrix_map::get_matrix_id($tf);
	}
	elsif ($org eq 'mouse') {
		$matrix_id = &mouse_tfbs_matrix_map::get_matrix_id($tf);
	}
	print "<table cellpadding=\"10\" border=\"0\"  width=$table_width>\n";
		print "<tbody>";
		print "<tr>\n";
			print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></font><br></td>\n";
			print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>&nbsp;&nbsp;Transcription factor binding site details for given gene <I>$gene_name (<a class=biocompendium href=\"http://www.ensembl.org/$org_mappings{$org}/geneview?gene=$gene\">$gene</a>)</I> and transcription factor : <I><a class=biocompendium href=\"http://jaspar.genereg.net/cgi-bin/jaspar_db.pl?ID=$matrix_id&rm=present&db=0\">$tf</a></I></font><br></td>\n";
		print "</tr>\n";
  my %socket_conf = &SocketConf::getSocketConf();	
	my $job_name = "tfbs";
	my $msg = $job_name."\n".$org."\n".$gene."\n".$matrix_id.$socket_conf{END_OF_MESSAGE_TAG}."\n";
#print "msg : $msg<br> matrix_id : $matrix_id<br>";	

	my $clint_socket = IO::Socket::INET->new( Proto => "tcp",
					   PeerAddr => $socket_conf{HOST},
					   PeerPort => $socket_conf{PORT}			
					 );	
	my $response = "";
	if ($gene && $matrix_id) {
		$response = $clint_socket->send($msg);
	}
	$/ = "_END_OF_MESSAGE_";
	$response = <$clint_socket>;
	chomp($response);
	$/ = "\n";
#print "response : $response<br>";
	close($clint_socket);
		my @entries = split /\n/, $response;
#		$response =~ s/\n/<br>/g;
#		$response =~ s/____/\t/g;
		print "<tr>\n";
			print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b></b></font></td>\n";
			print "<td><br>";
			print "<table cellspacing='0' border=1>\n";
				print "<tr><td class=biocompendium_header>Source</td><td class=biocompendium_header>Feature</td><td class=biocompendium_header>Start</td><td class=biocompendium_header>End</td><td class=biocompendium_header>Score</td><td class=biocompendium_header>Strand</td><td class=biocompendium_header>Frame</td><td class=biocompendium_header>Attribute</td><td class=biocompendium_header>Relative score</td></tr>\n";
				foreach my $e (@entries) {
					print "<tr><td class=biocompendium>TFBS</td><td class=biocompendium>TF binding site</td>";
						my @e = split /____/, $e;
						foreach my $td (@e) {
							print "<td class=biocompendium>$td</td>\n";
						} # foreach $td (@e) {
					print "</tr>\n";
				} # foreach my $e (@entries) {
#				print "<tr>\n";
#					print "<td class=biocompendium>$response";
#					print "</td>";
				print "</tr>\n";
			print "</table>";
		print "</td>";
	print "</tr>\n";	
	print "</tbody>";
print "</table>";	


} #
sub alert {
   print "Content-type: text/html\n\n";
   print "<script>alert('please at least select one tool!!!')</script>";
}
=end    BlockComment  # BlockCommentNo_1

=cut
