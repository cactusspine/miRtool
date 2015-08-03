#!/usr/bin/perl -w

#################################################################
## Developed by Venkata P. Satagopam venkata.satagopam@embl.de ##
## Disclaimer: Copy rights reserved by EMBL, please contact    ## 
## Venkata Satagopam prior to reuse any part of this code      ##
#################################################################

use strict;
use lib "./modules";

use IdMapper;
use DbmiRNA;
use Math::Combinatorics;
use List::Compare;
use Data::Dumper;

use CGI;

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
my $list = $q->param("list");

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
		$org = "";
	}
	if(!$input_type) {
		$input_type = "";
	}
	if(!$output_type) {
		$output_type = "";
	}
	if(!$text_area_ids) {
		$text_area_ids = "";
	}

my $host_name = "http://rschneider.embl.de/";
#my $URL_project = $host_name . "/biocompendium/";
my $URL_project = $host_name . "/";
my $URL_cgi = $host_name . "/cgi-bin/systec.cgi";
my $STITCH_URL = "http://stitch.embl.de";
my $chemistry_url = $URL_project . "/temp/structure/";
my $pubchem_url = "http://pubchem.ncbi.nlm.nih.gov/summary/summary.cgi?cid=";
my $dasty2das_client = "http://www.ebi.ac.uk/dasty/client/ebi.php";
my $outPutDir = "/var/www/html/rschneider/systec/database/temp/";
my $cgi_dir = "/var/www/cgi-bin/";
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
			-style=>{-src=>['http://rschneider.embl.de/systec/database/style/systec.css', 'http://rschneider.embl.de/systec/database/style/systec_popup.css']},
			-script=>[
					{-language=>'JAVASCRIPT',
					-src=>'http://rschneider.embl.de/systec/database/javascript/overlib.js'},
					{-language=>'JAVASCRIPT',
					-src=>'http://rschneider.embl.de/systec/database/javascript/tool_tip.js'},
					{-language=>'JAVASCRIPT',
					-src=>'http://rschneider.embl.de/systec/database/javascript/dynamic_file_upload.js'},
					{-language=>'JAVASCRIPT',
					-src=>'http://rschneider.embl.de/systec/database/javascript/id_type.js'},
					{-language=>'JAVASCRIPT',
					-src=>'http://rschneider.embl.de/systec/database/javascript/prototype.js'},
					{-language=>'JAVASCRIPT',
					-src=>'http://rschneider.embl.de/systec/database/javascript/effects.js'},
					{-language=>'JAVASCRIPT',
					-src=>'http://rschneider.embl.de/systec/database/javascript/dragdrop.js'},
					{-language=>'JAVASCRIPT',
					-src=>'http://rschneider.embl.de/systec/database/javascript/controls.js'},
					{-language=>'JAVASCRIPT',
					-src=>'http://rschneider.embl.de/systec/database/javascript/systec.js'},
					{-language=>'JAVASCRIPT',
					-src=>'http://rschneider.embl.de/systec/database/javascript/systec_popup.js'},
					{-language=>'JAVASCRIPT',
					-src=>'http://rschneider.embl.de/systec/database/javascript/checkboxes.js'},
				],
			-onload=>'return toggleAll(\'collapse\')'
		    );

# this line include the form action, cgi script etc, ...very nice one
	my $form_name = "systec";
	my $method = "POST";
	my $action = "/cgi-bin/systec.cgi";
	my $encoding = "multipart/form-data";
	print $q->startform($method, $action, $encoding, "name=\"$form_name\"");

	my %tax_mappings = (
			9606  => 'human',
			10090 => 'mouse',
			4932  => 'yeast',

			'human'  => 9606,
			'mouse'  => 10090,
			'yeast'  => 4932
		       ); 		     
	
	my %ensembl_mappings = (
			3 => 'Rattus_norvegicus',
			4 => 'Takifugu_rubripes',
			5 => 'Anopheles_gambiae',
			16 => 'Xenopus_tropicalis',
			18 => 'Ciona_intestinalis',
			22 => 'Homo_sapiens',
			27 => 'Ciona_savignyi',
			29 => 'Aedes_aegypti',
			31 => 'Macaca_mulatta',
			33 => 'Echinops_telfairi',
			34 => 'Oryctolagus_cuniculus',
			35 => 'Dasypus_novemcinctus',
			36 => 'Gasterosteus_aculeatus',
			37 => 'Oryzias_latipes',
			38 => 'Pan_troglodytes',
			39 => 'Canis_familiaris',
			42 => 'Gallus_gallus',
			43 => 'Ornithorhynchus_anatinus',
			44 => 'Saccharomyces_cerevisiae',
			46 => 'Monodelphis_domestica',
			48 => 'Tupaia_belangeri',
			49 => 'Erinaceus_europaeus',
			51 => 'Otolemur_garnettii',
			52 => 'Spermophilus_tridecemlineatus',
			53 => 'Myotis_lucifugus',
			55 => 'Sorex_araneus',
			56 => 'Danio_rerio',
			57 => 'Mus_musculus',
			58 => 'Microcebus_murinus',
			60 => 'Pongo_pygmaeus',
			61 => 'Equus_caballus',
			62 => 'Drosophila_melanogaster',
			63 => 'Ancestral_sequences',
			64 => 'Bos_taurus',
			65 => 'Tetraodon_nigroviridis',
			66 => 'Felis_catus',
			67 => 'Ochotona_princeps',
			68 => 'Caenorhabditis_elegans',
			69 => 'Cavia_porcellus',
			70 => 'Dipodomys_ordii',
			71 => 'Pteropus_vampyrus',
			72 => 'Tursiops_truncatus',
			73 => 'Vicugna_pacos',
			74 => 'Procavia_capensis',
			75 => 'Loxodonta_africana',
			76 => 'Tarsius_syrichta'			
	       	);	
	my %org_mappings = (
			'human' => 'Homo_sapiens',
			'mouse' => 'Mus_musculus',
			'yeast' => 'Saccharomyces_cerevisiae',
		       ); 		     

	my %colors = (
			1  => '0,0,0',
			2  => '255,0,0',
			3  => '0,100,0',
			4  => '25,25,112',
			5  => '0,255,0',
			6  => '139,134,78',
			7  => '139,58,58',
			8  => '255,20,147',
			9  => '255,0,255',
			10 => '155,48,255',
			11 => '150,150,150',
			12 => '49,79,79',
			13 => '100,149,237',
			14 => '106,90,205',
			15 => '0,0,255',
			16 => '0,255,255',
			17 => '0,255,0',
			18 => '255,255,0',
			19 => '255,165,0',
			20 => '255,99,71',
			21 => '176,48,96',
			22 => '0,191,255',
			23 => '112,128,144',
			24 => '65,105,225',
			25 => '0,206,209',
			26 => '85,107,47',
			27 => '124,252,0',
			28 => '184,134,11',
			29 => '255,105,180',
			30 => '24,116,205',
			31 => '0,245,255',
			32 => '69,139,116',
			33 => '255,140,0',
			34 => '0,104,130',
			35 => '139,26,26',
			36 => '105,139,34',
			37 => '77,77,77',
			38 => '34,139,34',
			39 => '210,105,30',
			40 => '0,139,0',
			41 => '85,26,139',
			42 => '139,54,38',
			43 => '240,128,128',
			44 => '0,134,139',
			45 => '54,100,139',
			46 => '208,32,144',
			47 => '138,43,226',
			48 => '205,133,63',
			49 => '32,178,170',
			50 => '70,130,180'
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
	my $org = "human";

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
			@gene_list = &nonRedundantList(\@gene_list);	
		} # foreach my $gene (@temp_gene_list) {
	}
	else {
		my $file = $ids_file;
#print "input_type : $input_type, org : $org, file : $file<br>";
		@gene_list = &get_gene_list($org, $file, $input_type, $org, $session_dir);
#print "gene_list : @gene_list<br>";
	}
#print "gene_list : @gene_list<br>";
	
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
		print "</table><br></td>";
	print "</tr>";

	close(FH_MYSQL);
	system("/usr/bin/mysql -u srk -psrk -h 10.79.5.221 < $mysql_file");
	&table_view(0, $session, $input_type, 'mirna_name', 'asc');
} # sub process_genelists {


sub get_gene_list {
	my ($org, $file, $input_type, $primary_org, $session_dir) = @_;
	my $file_name = "";
	if ($file=~m/^.*(\\|\/)(.*)/){ # strip the remote path and keep the file_name 
	       	$file_name = $2;
       	}
       	else {
	       	$file_name = $file;
       	}
	my $dir_local_file = $session_dir . "gene_list__0";
#print "dir_local_file : $dir_local_file<br>";
	
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
	if ($input_type eq "pseudogene_id" || $input_type eq "mirbase_name" || $input_type eq "mirbase_id" || $input_type eq "long_ncrna_id" || $input_type eq "antisense_rna_id" || $input_type eq "sirna_id" || $input_type eq "snorna_id" || $input_type eq "snrna_id" || $input_type eq "trna_id" || $input_type eq "rrna_id" || $input_type eq "pirna_id") {
		@ensembl_genes = @id_list;
	} # if ($input_type eq "ensembl_gene_id" ) {
	else {
		@ensembl_genes = &IdMapper::get_ensembl_genes($org, \@id_list, $input_type, $primary_org);
	} # else 
#print "ensembl_genes : @ensembl_genes<br>";
	@ensembl_genes = &nonRedundantList(\@ensembl_genes);
	return @ensembl_genes;
} # sub get_gene_list {


sub table_view {
	my ($position, $session, $input_type, $sort_by_field_name, $asc_or_desc) = @_;
	my $list_name = "gene_list__0";
	my $org = "human";
	my $section="biodb";
#	my $banner = &get_browse_banner("");
#print "session : $session<br>";
#print "org : $org<br>";
#print "list_name : $list_name<br>";
#print "input_type : $input_type<br>";
	my $result_hash = undef;
	if($input_type eq "mirbase_name") {
		$result_hash = &DbmiRNA::GetTableViewInfo($input_type, $asc_or_desc, $session, $list_name);
	}
	else {
		$result_hash = &DbmiRNA::GetGeneCentricTableViewInfo($input_type, $asc_or_desc, $session, $list_name);
	}
#	elsif($org eq "mouse") {
#		$result_hash = &DbMouseGeneName::GetTableViewInfo($sort_by_field_name, $asc_or_desc, $session, $list_name);
#	}
#	elsif($org eq "yeast") {
#		$result_hash = &DbYeastGeneName::GetTableViewInfo($sort_by_field_name, $asc_or_desc, $session, $list_name);
#	}
	my %result_hash = %$result_hash;
	my $mirna_hash = $result_hash->{'mirna_hash'};
	my %mirna_hash = %$mirna_hash;

	my $target_hash = $result_hash->{'target_hash'};
	my %target_hash = %$target_hash;

	my $mirna_size_hash = $result_hash->{'mirna_size_hash'};
	my %mirna_size_hash = %$mirna_size_hash;
	my @mirna_size_hash_keys = keys %mirna_size_hash;
	my $mirna_size_hash_size = scalar(@mirna_size_hash_keys); 
	
	my $gene_size_hash = $result_hash->{'gene_size_hash'};
	my %gene_size_hash = %$gene_size_hash;
	my @gene_size_hash_keys = keys %gene_size_hash;
	my $gene_size_hash_size = scalar(@gene_size_hash_keys); 
	
	my $transcript_size_hash = $result_hash->{'transcript_size_hash'};
	my %transcript_size_hash = %$transcript_size_hash;
	my @transcript_size_hash_keys = keys %transcript_size_hash;
	my $transcript_size_hash_size = scalar(@transcript_size_hash_keys); 
	
	my @keys = ();
	if($input_type eq "mirbase_name") {
		 @keys = keys %mirna_hash;
	}
	else {
		 @keys = keys %target_hash;
	}
	@keys = sort @keys;
	my $size = scalar(@keys);
print "<table cellpadding=\"10\" border=\"0\"  width=$table_width>\n";
	print "<tbody>";
			print "<tr>\n";
				print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description: </b></font></td>\n";
				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><br><b>Information from various biological sources in a short tabular view</b></font><br><br></td>\n";
			print "</tr>\n";
			print "<tr>\n";
				print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><br><b>Input</b></font></td>\n";
	if(($input_type eq "mirbase_name")||($input_type eq "mirbase_acc")) {
				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>No. of miRNAs : $mirna_size_hash_size</b></font><br></td>\n";
	}
	else {
				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>No. of Genes : $gene_size_hash_size</b></font><br></td>\n";
	}
			print "</tr>\n";

#			print "<tr>\n";
#				print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Legend</b></font></td>\n";
#				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><i>: The following table is sortable</i><br></font></td>\n";
#			print "</tr>\n";
	my $numdisplay = 30;
	$position++;
	$position--;
	
	my @subSet = splice(@keys, $position, $numdisplay);
	if($input_type eq "mirbase_name") {
		my $call_sub_table_view = &sub_table_view(\@subSet, $session, $list_name, $org, \%result_hash);
	}
	else {
		my $call_sub_table_view = &sub_table_view_gene_centric(\@subSet, $session, $list_name, $org, \%result_hash);
	}
	my $total = $size;
	my ($nextstring,$prevstring,$firststring,$laststring,$startno,$endno) = &BuildNextPrevLinksForKeywordSearchSort("true", $total, $numdisplay, $position, $section, $session,$input_type, $sort_by_field_name, $asc_or_desc);
	print "<br>\n";
	print "<table cellspacing='0' border='0' align='right'>\n";
			print "<tr>\n";
				print "<td align=\"right\"><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>&nbsp;&nbsp;&nbsp;&nbsp;$firststring</b></font></td>\n";
				print "<td align=\"right\"><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>&nbsp;&nbsp;&nbsp;&nbsp;$prevstring</b></font></td>\n";
				print "<td align=\"right\"><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>&nbsp;&nbsp;&nbsp;&nbsp;$nextstring</b></font></td>\n";
				print "<td align=\"right\"><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>&nbsp;&nbsp;&nbsp;&nbsp;$laststring</b></font></td>\n";
			print "</tr>\n";
		print "</tbody>\n";
	print "</table>\n";
		
	
## srk srk srk
} # sub table_view


sub sub_table_view {
	my ($keys, $session, $list_name, $org, $result_hash) = @_;

	my @keys = @$keys;
	my %result_hash = %$result_hash;

	my $mirna_hash = $result_hash->{'mirna_hash'};
	my %mirna_hash = %$mirna_hash;

	my $target_hash = $result_hash->{'target_hash'};
	my %target_hash = %$target_hash;

	print "<table cellpadding=\"10\" border=\"0\"  width=1200>\n";
		print "<tbody>";
			my $imgNo = 0;
			print "<tr>\n";
				print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></font></td>\n";
				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Details of miRNA Targets</b></font><br></td>\n";
			print "</tr>\n";
			print "<tr>\n";
				print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"></font></td>\n";
				print "<td><br><a href=\"#\" onclick=\"return toggleAll(\'expand\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'expand\' onClick=\'changeImage(\"expand\")\'></a> <font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Expand All</b></font><a href=\"#\" onclick=\"return toggleAll(\'collapse\')\"> <img alt=\"\" src=\"/images/minus.gif\" name=\'collapse\' onClick=\'changeImage(\"collapse\")\'></a> <font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Collapse All</b></font><br></td>\n";
			print "</tr>\n";
			print "<tr>\n";
				print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>miRNA & Targets: </b></font></td>\n";
				print "<td><br>";
					print "<table cellspacing='2' border='0'>\n";

					my $i = 0;
					my $z = 0;
					foreach my $mirna_name (@keys) {
						$z++;
						my $mirna_acc = $mirna_hash{$mirna_name}{'mirna_acc'};
						my $mirna_chr = $mirna_hash{$mirna_name}{'mirna_chr'};
						my $mirna_start = $mirna_hash{$mirna_name}{'mirna_start'};
						my $mirna_stop = $mirna_hash{$mirna_name}{'mirna_stop'};
						my $mirna_strand = $mirna_hash{$mirna_name}{'mirna_strand'};
						my $mirna_mirbase = $mirna_hash{$mirna_name}{'mirna_mirbase'};
						my $mirna_targetscan = $mirna_hash{$mirna_name}{'mirna_targetscan'};
						my $mirna_pictar = $mirna_hash{$mirna_name}{'mirna_pictar'};
						my $mirna_starbase = $mirna_hash{$mirna_name}{'mirna_starbase'};
						my $mirna_mirdb = $mirna_hash{$mirna_name}{'mirna_mirdb'};
						my $mirna_score = $mirna_hash{$mirna_name}{'mirna_score'}; 

						my %sorted_target_hash = ();
						foreach my $transcript_id ( keys %{$target_hash{$mirna_name}}) {
							my $transcript_score = $target_hash{$mirna_name}{$transcript_id}{'transcript_score'};
							$sorted_target_hash{$transcript_id} = $transcript_score;
						} # foreach my $transcript_id ( keys %{$target_hash{$mirna_name}}) {
							
						my $target_details = "";
						foreach my $transcript_id (sort {$sorted_target_hash{$b}<=>$sorted_target_hash{$a}} keys %sorted_target_hash) {
					        	my $transcript_id =  $target_hash{$mirna_name}{$transcript_id}{'transcript_id'} ; 
							my $transcript_start =  $target_hash{$mirna_name}{$transcript_id}{'transcript_start'} ; 
							my $transcript_stop =  $target_hash{$mirna_name}{$transcript_id}{'transcript_stop'} ; 
							my $transcript_name =  $target_hash{$mirna_name}{$transcript_id}{'transcript_name'} ; 
							my $transcript_status =  $target_hash{$mirna_name}{$transcript_id}{'transcript_status'} ; 
							my $transcript_microcosm =  $target_hash{$mirna_name}{$transcript_id}{'transcript_microcosm'} ; 
							my $transcript_targetscan =  $target_hash{$mirna_name}{$transcript_id}{'transcript_targetscan'} ;
							my $transcript_pictar =  $target_hash{$mirna_name}{$transcript_id}{'transcript_pictar'} ; 
							my $transcript_starbase =  $target_hash{$mirna_name}{$transcript_id}{'transcript_starbase'} ; 
							my $transcript_mirdb =  $target_hash{$mirna_name}{$transcript_id}{'transcript_mirdb'} ; 
							my $transcript_score =  $target_hash{$mirna_name}{$transcript_id}{'transcript_score'} ; 
							my $gene_id =  $target_hash{$mirna_name}{$transcript_id}{'gene_id'} ; 
							my $gene_chr =  $target_hash{$mirna_name}{$transcript_id}{'gene_chr'} ; 
							my $gene_start =  $target_hash{$mirna_name}{$transcript_id}{'gene_start'} ; 
							my $gene_stop =  $target_hash{$mirna_name}{$transcript_id}{'gene_stop'} ; 
							my $gene_strand =  $target_hash{$mirna_name}{$transcript_id}{'gene_strand'} ; 
							my $gene_name =  $target_hash{$mirna_name}{$transcript_id}{'gene_name'} ; 
							my $description =  $target_hash{$mirna_name}{$transcript_id}{'description'} ; 
							my $gene_biotype =  $target_hash{$mirna_name}{$transcript_id}{'gene_biotype'} ; 
							my $gene_status =  $target_hash{$mirna_name}{$transcript_id}{'gene_status'} ; 
							my $transcript_count =  $target_hash{$mirna_name}{$transcript_id}{'transcript_count'} ; 
	
							$i++;
							my $bg;
							if($i%2==0) {
								$bg="#D4EDF4";
							}
							else {
								$bg="#cfc3f3";
							}
#https://biocompendium.embl.de/cgi-bin/biocompendium.cgi?section=summary_sheet&gene=ENSG00000097046&org=human
							$target_details .= "<tr bgcolor=\"$bg\">\n";
							$target_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><a class=biocompendium href=\"https://biocompendium.embl.de/cgi-bin/biocompendium.cgi?section=summary_sheet&gene=$gene_id&org=human\">$gene_name</a></font></td>\n";
#http://www.ensembl.org/Homo_sapiens/Transcript/Summary?t=ENST00000296877
							$target_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><a class=biocompendium href=\"http://www.ensembl.org/Homo_sapiens/Transcript/Summary?t=$transcript_id\">$transcript_id</a></font></td>\n";
							$target_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$gene_chr</font></td>\n";
							$target_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$transcript_start</font></td>\n";
							$target_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$transcript_stop</font></td>\n";
							$target_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$gene_strand</font></td>\n";
							$target_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$transcript_microcosm</font></td>\n";
							$target_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$transcript_targetscan</font></td>\n";
							$target_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$transcript_pictar</font></td>\n";
							$target_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$transcript_starbase</font></td>\n";
							$target_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$transcript_mirdb</font></td>\n";
							$target_details .= "</tr>\n";
						} # foreach my $transcript_id (sort {$sorted_target_hash{$a}<=>$sorted_target_hash{$b}} keys %sorted_target_hash) {


						print "<tbody>";
							 print "<tr>\n";
								my $toggle = "target" . $mirna_name;
								$imgNo++;
#http://www.mirbase.org/cgi-bin/mirna_entry.pl?acc=MI0000651
								print "<td colspan=2 width=\"12%\" bgcolor= #dcdcdc><a href=\"#\" onclick=\"return toggleItem(\'$toggle\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>#miRNA: <a class=biocompendium href=\"http://www.mirbase.org/cgi-bin/mirna_entry.pl?acc=$mirna_acc\">$mirna_name</a></b></font>";
								print "</td>\n";
								print "<td bgcolor= #dcdcdc><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Chr: $mirna_chr</b></font></td>\n";
								print "<td bgcolor= #dcdcdc><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Start: $mirna_start</b></font></td>\n";
								print "<td bgcolor= #dcdcdc><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Stop: $mirna_stop</b></font></td>\n";
								print "<td colspan=6 bgcolor= #dcdcdc><font face=\"Arial\" size=\"2\" color=\"#000000\" ><b>Strand: $mirna_strand</b></font></td>\n";
							print "</tr>\n";
						print "</tbody>";
						print "<tbody class=\"collapse_obj\" id=\"$toggle\">\n";
							print "<tr>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Gene </b></font></td>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>mRNA ID </b></font></td>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Gene chr </b></font></td>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>mRNA start</b></font></td>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>mRNA stop</b></font></td>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Strand</b></font></td>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Microcosm</b></font></td>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>TargetScan</b></font></td>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>picTar</b></font></td>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>starBase</b></font></td>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>miRDB</b></font></td>\n";
							print "</tr>\n";
							print "$target_details";
							print "<tr><td>&nbsp;</td><td></td></tr>";
						print "</tbody>\n";
					} # foreach my $cluster_id (@cluster_ids) {
				print "</table>\n";
			print "<br></td>";
		print "</tr>\n";
	print "</table>\n";
}# sub sub_table_view {

sub sub_table_view_gene_centric {
	my ($keys, $session, $list_name, $org, $result_hash) = @_;

	my @keys = @$keys;
	my %result_hash = %$result_hash;

	my $mirna_hash = $result_hash->{'mirna_hash'};
	my %mirna_hash = %$mirna_hash;

	my $target_hash = $result_hash->{'target_hash'};
	my %target_hash = %$target_hash;

	print "<table cellpadding=\"10\" border=\"0\"  width=1200>\n";
		print "<tbody>";
			my $imgNo = 0;
			print "<tr>\n";
				print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></font></td>\n";
				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Details of miRNA Targets</b></font><br></td>\n";
			print "</tr>\n";
			print "<tr>\n";
				print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"></font></td>\n";
				print "<td><br><a href=\"#\" onclick=\"return toggleAll(\'expand\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'expand\' onClick=\'changeImage(\"expand\")\'></a> <font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Expand All</b></font><a href=\"#\" onclick=\"return toggleAll(\'collapse\')\"> <img alt=\"\" src=\"/images/minus.gif\" name=\'collapse\' onClick=\'changeImage(\"collapse\")\'></a> <font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Collapse All</b></font><br></td>\n";
			print "</tr>\n";
			print "<tr>\n";
				print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>miRNA & Targets: </b></font></td>\n";
				print "<td><br>";
					print "<table cellspacing='2' border='0'>\n";

					my $i = 0;
					my $z = 0;
					foreach my $transcript_id (@keys) {
						$z++;
my $transcript_start =  $target_hash{$transcript_id}{'transcript_start'};
my $transcript_stop =  $target_hash{$transcript_id}{'transcript_stop'};
my $transcript_name =  $target_hash{$transcript_id}{'transcript_name'};
my $transcript_status =  $target_hash{$transcript_id}{'transcript_status'};
my $transcript_microcosm =  $target_hash{$transcript_id}{'transcript_microcosm'};
my $transcript_targetscan =  $target_hash{$transcript_id}{'transcript_targetscan'};
my $transcript_pictar =  $target_hash{$transcript_id}{'transcript_pictar'};
my $transcript_starbase =  $target_hash{$transcript_id}{'transcript_starbase'};
my $transcript_mirdb =  $target_hash{$transcript_id}{'transcript_mirdb'};
my $transcript_score =  $target_hash{$transcript_id}{'transcript_score'};
my $gene_id =  $target_hash{$transcript_id}{'gene_id'};
my $gene_chr =  $target_hash{$transcript_id}{'gene_chr'};
my $gene_start =  $target_hash{$transcript_id}{'gene_start'};
my $gene_stop =  $target_hash{$transcript_id}{'gene_stop'};
my $gene_strand =  $target_hash{$transcript_id}{'gene_strand'};
my $gene_name =  $target_hash{$transcript_id}{'gene_name'};
my $description =  $target_hash{$transcript_id}{'description'};
my $gene_biotype =  $target_hash{$transcript_id}{'gene_biotype'};
my $gene_status =  $target_hash{$transcript_id}{'gene_status'};
my $transcript_count =  $target_hash{$transcript_id}{'transcript_count'};


						my %sorted_mirna_hash = ();
						foreach my $mirna_name ( keys %{$mirna_hash{$transcript_id}}) {
							my $mirna_score = $mirna_hash{$transcript_id}{$mirna_name}{'mirna_score'};
							$sorted_mirna_hash{$mirna_name} = $mirna_score;
						} # foreach my $transcript_id ( keys %{$target_hash{$mirna_name}}) {
							
						my $mirna_details = "";
						foreach my $mirna_name (sort {$sorted_mirna_hash{$b}<=>$sorted_mirna_hash{$a}} keys %sorted_mirna_hash) {
					        	my $mirna_acc =  $mirna_hash{$transcript_id}{$mirna_name}{'mirna_acc'} ; 
					        	my $mirna_chr =  $mirna_hash{$transcript_id}{$mirna_name}{'mirna_chr'} ; 
					        	my $mirna_start =  $mirna_hash{$transcript_id}{$mirna_name}{'mirna_start'} ; 
					        	my $mirna_stop =  $mirna_hash{$transcript_id}{$mirna_name}{'mirna_stop'} ; 
					        	my $mirna_strand =  $mirna_hash{$transcript_id}{$mirna_name}{'mirna_strand'} ; 
					        	my $mirna_mirbase =  $mirna_hash{$transcript_id}{$mirna_name}{'mirna_mirbase'} ; 
					        	my $mirna_targetscan =  $mirna_hash{$transcript_id}{$mirna_name}{'mirna_targetscan'} ; 
					        	my $mirna_pictar =  $mirna_hash{$transcript_id}{$mirna_name}{'mirna_pictar'} ; 
					        	my $mirna_starbase =  $mirna_hash{$transcript_id}{$mirna_name}{'mirna_starbase'} ; 
					        	my $mirna_mirdb =  $mirna_hash{$transcript_id}{$mirna_name}{'mirna_mirdb'} ; 
					        	my $mirna_score =  $mirna_hash{$transcript_id}{$mirna_name}{'mirna_score'} ; 
	
							$i++;
							my $bg;
							if($i%2==0) {
								$bg="#D4EDF4";
							}
							else {
								$bg="#cfc3f3";
							}

#https://biocompendium.embl.de/cgi-bin/biocompendium.cgi?section=summary_sheet&gene=ENSG00000097046&org=human
							$mirna_details .= "<tr bgcolor=\"$bg\">\n";
							$mirna_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><a class=biocompendium href=\"http://www.mirbase.org/cgi-bin/mirna_entry.pl?acc=$mirna_acc\">$mirna_name</a></font></td>\n";
#http://www.ensembl.org/Homo_sapiens/Transcript/Summary?t=ENST00000296877
							$mirna_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$mirna_chr</font></td>\n";
							$mirna_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$mirna_start</font></td>\n";
							$mirna_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$mirna_stop</font></td>\n";
							$mirna_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$mirna_strand</font></td>\n";
							$mirna_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$mirna_mirbase</font></td>\n";
							$mirna_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$mirna_targetscan</font></td>\n";
							$mirna_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$mirna_pictar</font></td>\n";
							$mirna_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$mirna_starbase</font></td>\n";
							$mirna_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$mirna_mirdb</font></td>\n";
							$mirna_details .= "</tr>\n";
						} # foreach my $mirna_name (sort {$sorted_mirna_hash{$b}<=>$sorted_mirna_hash{$a}} keys %sorted_mirna_hash) {


						print "<tbody>";
							 print "<tr>\n";
								my $toggle = "target" . $transcript_id;
								$imgNo++;
#http://www.mirbase.org/cgi-bin/mirna_entry.pl?acc=MI0000651
								print "<td  width=\"12%\" bgcolor= #dcdcdc><a href=\"#\" onclick=\"return toggleItem(\'$toggle\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>#Gene: <a class=biocompendium href=\"https://biocompendium.embl.de/cgi-bin/biocompendium.cgi?section=summary_sheet&gene=$gene_id&org=human\">$gene_name</a></b></font>";
								print "</td>\n";
								print "<td bgcolor= #dcdcdc><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>mRNA: <a class=biocompendium href=\"http://www.ensembl.org/Homo_sapiens/Transcript/Summary?t=$transcript_id\">$transcript_id</a></b></font></td>\n";
								print "<td bgcolor= #dcdcdc><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Chr: $gene_chr</b></font></td>\n";
								print "<td bgcolor= #dcdcdc><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Start: $transcript_start</b></font></td>\n";
								print "<td bgcolor= #dcdcdc><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Stop: $transcript_stop</b></font></td>\n";
								print "<td bgcolor= #dcdcdc><font face=\"Arial\" size=\"2\" color=\"#000000\" ><b>Strand: $gene_strand</b></font></td>\n";
								print "<td colspan=4 bgcolor= #dcdcdc><font face=\"Arial\" size=\"2\" color=\"#000000\" ><b>Description: $description</b></font></td>\n";
							print "</tr>\n";
						print "</tbody>";
						print "<tbody class=\"collapse_obj\" id=\"$toggle\">\n";
							print "<tr>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>miRNA</b></font></td>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>miRNA chr</b></font></td>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>miRNA start</b></font></td>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>miRNA stop</b></font></td>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Strand</b></font></td>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>miRBase</b></font></td>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>TargetScan</b></font></td>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>picTar</b></font></td>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>starBase</b></font></td>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>miRDB</b></font></td>\n";
							print "</tr>\n";
							print "$mirna_details";
							print "<tr><td>&nbsp;</td><td></td></tr>";
						print "</tbody>\n";
					} # foreach my $cluster_id (@cluster_ids) {
				print "</table>\n";
			print "<br></td>";
		print "</tr>\n";
	print "</table>\n";
}# sub_table_view_gene_centric


#sub sub_table_view {
#	my ($keys, $session, $list_name, $org, $result_hash) = @_;
#
#	my @keys = @$keys;
#	my %result_hash = %$result_hash;
#
#			print "<tr>\n";
#				print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b></b></font></td>\n";
#				print "<td><br>";
#						print "<table cellspacing='0'>\n";
#		print "<tr>\n";
#			print "<td>";
#				print "<table border=0 cellspacing='1'>\n";
#
#					my $asc_link_img = "desc.png";
#					my $desc_link_img = "asc.png";
#					my $gene_asc_desc = "<table><tr><td>Gene</td><td><table><tr><td><a href=\"$URL_cgi?section=biodb&pos=0&org=$org&session=$session&list=$list_name&sort=gene&ad=desc\"><img alt=\"\" src=\"/images/$desc_link_img\" width=$hyper_link_img_width height=$hyper_link_img_height border='0'></a></td></tr><tr><td><a href=\"$URL_cgi?section=biodb&pos=0&org=$org&session=$session&list=$list_name&sort=gene&ad=asc\"><img alt=\"\" src=\"/images/$asc_link_img\" width=$hyper_link_img_width height=$hyper_link_img_height border='0'></a></td></tr></table></td></tr></table>";
##					my $name_asc_desc = "<table><tr><td>Name</td><td><table><tr><td><a href=\"$URL_cgi?section=biodb&pos=0&org=$org&session=$session&list=$list_name&sort=name&ad=desc\"><img alt=\"\" src=\"/images/$desc_link_img\" width=$hyper_link_img_width height=$hyper_link_img_height border='0'></a></td></tr><tr><td><a href=\"$URL_cgi?section=biodb&pos=0&org=$org&session=$session&list=$list_name&sort=name&ad=asc\"><img alt=\"\" src=\"/images/$asc_link_img\" width=$hyper_link_img_width height=$hyper_link_img_height border='0'></a></td></tr></table></td></tr></table>";
#					my $description_asc_desc = "<table><tr><td>Description</td><td><table><tr><td><a href=\"$URL_cgi?section=biodb&pos=0&org=$org&session=$session&list=$list_name&sort=description&ad=desc\"><img alt=\"\" src=\"/images/$desc_link_img\" width=$hyper_link_img_width height=$hyper_link_img_height border='0'></a></td></tr><tr><td><a href=\"$URL_cgi?section=biodb&pos=0&org=$org&session=$session&list=$list_name&sort=description&ad=asc\"><img alt=\"\" src=\"/images/$asc_link_img\" width=$hyper_link_img_width height=$hyper_link_img_height border='0'></a></td></tr></table></td></tr></table>";
#
#
#					 print "<tr>\n";


#sub sub_table_view {
#	my ($keys, $session, $list_name, $org, $result_hash) = @_;
#
#	my @keys = @$keys;
#	my %result_hash = %$result_hash;
#
#			print "<tr>\n";
#				print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b></b></font></td>\n";
#				print "<td><br>";
#						print "<table cellspacing='0'>\n";
#		print "<tr>\n";
#			print "<td>";
#				print "<table border=0 cellspacing='1'>\n";
#
#					my $asc_link_img = "desc.png";
#					my $desc_link_img = "asc.png";
#					my $gene_asc_desc = "<table><tr><td>Gene</td><td><table><tr><td><a href=\"$URL_cgi?section=biodb&pos=0&org=$org&session=$session&list=$list_name&sort=gene&ad=desc\"><img alt=\"\" src=\"/images/$desc_link_img\" width=$hyper_link_img_width height=$hyper_link_img_height border='0'></a></td></tr><tr><td><a href=\"$URL_cgi?section=biodb&pos=0&org=$org&session=$session&list=$list_name&sort=gene&ad=asc\"><img alt=\"\" src=\"/images/$asc_link_img\" width=$hyper_link_img_width height=$hyper_link_img_height border='0'></a></td></tr></table></td></tr></table>";
##					my $name_asc_desc = "<table><tr><td>Name</td><td><table><tr><td><a href=\"$URL_cgi?section=biodb&pos=0&org=$org&session=$session&list=$list_name&sort=name&ad=desc\"><img alt=\"\" src=\"/images/$desc_link_img\" width=$hyper_link_img_width height=$hyper_link_img_height border='0'></a></td></tr><tr><td><a href=\"$URL_cgi?section=biodb&pos=0&org=$org&session=$session&list=$list_name&sort=name&ad=asc\"><img alt=\"\" src=\"/images/$asc_link_img\" width=$hyper_link_img_width height=$hyper_link_img_height border='0'></a></td></tr></table></td></tr></table>";
#					my $description_asc_desc = "<table><tr><td>Description</td><td><table><tr><td><a href=\"$URL_cgi?section=biodb&pos=0&org=$org&session=$session&list=$list_name&sort=description&ad=desc\"><img alt=\"\" src=\"/images/$desc_link_img\" width=$hyper_link_img_width height=$hyper_link_img_height border='0'></a></td></tr><tr><td><a href=\"$URL_cgi?section=biodb&pos=0&org=$org&session=$session&list=$list_name&sort=description&ad=asc\"><img alt=\"\" src=\"/images/$asc_link_img\" width=$hyper_link_img_width height=$hyper_link_img_height border='0'></a></td></tr></table></td></tr></table>";
#
#
#					 print "<tr>\n";
#						print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>$name_asc_desc </b></font></td>\n";
#						print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>$description_asc_desc </b></font></td>\n";		
#						print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>$gene_asc_desc </b></font></td>\n";
#					print "</tr><tbody>\n";
#					my $i = 0;
#					foreach my $k (@keys) {
#						$i++;
#						my $bg;
#						if($i%2==0) {
#							$bg="#D4EDF4";
#						}
#						else {
#							$bg="#cfc3f3";
#						}
#						my $name = $result_hash{$k}{name};
#						my $description = $result_hash{$k}{description};
#						my $gene = $result_hash{$k}{gene};
#						if ($name eq "" || $description eq "") {
#							if($org eq "mouse") {
#use DbMouseGeneNameDes;
#								my $gene_name_des_obj = new DbMouseGeneNameDes($gene);
#								$name = $gene_name_des_obj->{name};
#								$description = $gene_name_des_obj->{description};
#							}
#						}
#						my $gene_url = "http://www.ensembl.org/$org_mappings{$org}/geneview?gene=$gene";
#
#							print "<tr bgcolor=\"$bg\">\n";
#								print "<td width=10%><font face=\"Arial\" size=\"2\" color=\"#000000\"><a href=\"$URL_cgi?section=summary_sheet&gene=$gene&org=$org\">$name</a></font></td>\n";
#								print "<td width=75%><font face=\"Arial\" size=\"2\" color=\"#000000\">$description</font></td>";
#								print "<td width=15%><font face=\"Arial\" size=\"2\" color=\"#000000\"><a class=biocompendium href=\"$gene_url\">$gene</font></td>";
#							print "</tr>\n";
#					} # foreach my $k (@keys) {
#				print "</tbody></table>\n";
#			print "</tr>\n";
#	print "</table>\n";		
#} # sub sub_table_view {
#
#sub sub_table_view_with_out_sort {
#	my ($ids, $org) = @_;
#use DbHumanSummarySheet;
#	my @ids = @$ids;
#	my $size = @ids;
#	my $rowSpan = $size;
#	$rowSpan++;
#
#			print "<tr>\n";
#				print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Hits</b></font></td>\n";
#				print "<td><br>";
#						print "<table cellspacing='0'>\n";
#		print "<tr>\n";
#			print "<td>";
#				print "<table border=0 cellspacing='1'>\n";
#					 print "<tr>\n";
#						print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Name </b></font></td>\n";		
#						print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description </b></font></td>\n";
#						print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Gene </b></font></td>\n";
#					print "</tr><tbody>\n";
#					my $i = 0;
#					foreach my $id (@ids) {
#						$i++;
#						my $bg;
#						if($i%2==0) {
#							$bg="#D4EDF4";
#						}
#						else {
#							$bg="#cfc3f3";
#						}
#						
#						my $summary_sheet = 0;
#						my $gene_name_obj = 0;
#						if ($org eq 'human') {
#							$summary_sheet = new DbHumanSummarySheet($id);
#						}
#
#						my $description = $summary_sheet->{Description};
#						my $gene = $summary_sheet->{Gene};
#						if ($org eq 'human') {
#							$gene_name_obj = new DbHumanGeneName($gene);
#						}
#
#						my $name = $gene_name_obj->{name};
#						my $gene_url = "http://www.ensembl.org/$org_mappings{$org}/geneview?gene=$gene";
#
#							print "<tr bgcolor=\"$bg\">\n";
#								print "<td width=10%><font face=\"Arial\" size=\"2\" color=\"#000000\"><a href=\"$URL_cgi?section=summary_sheet&gene=$gene&org=$org\">$name</a></font></td>\n";
#								print "<td width=75%><font face=\"Arial\" size=\"2\" color=\"#000000\">$description</font></td>";
#								print "<td width=15%><font face=\"Arial\" size=\"2\" color=\"#000000\"><a class=biocompendium href=\"$gene_url\">$gene</font></td>";
#							print "</tr>\n";
#					} # foreach my $k (@keys) {
#				print "</tbody></table>\n";
#			print "</tr>\n";
#	print "</table>\n";		
#} # sub sub_table_view_with_sort {


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
