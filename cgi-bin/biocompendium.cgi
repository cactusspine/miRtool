#!/usr/bin/perl -w

#################################################################
##							       																			   ##	
## Developed by Venkata P. Satagopam as part of his PhD thesis ##
##		 venkata.satagopam@embl.de		   												 ##
##							       																				 ##
## Disclaimer: Copy rights reserved by EMBL, please contact    ## 
##	       Venkata Satagopam  prior to reuse any part      		 ##
##	     of this code 				       													 ##
##							       																				 ##
#################################################################

use strict;
use lib "/g/projects_rs/biocompendium/modules";

use Reflect;
use IdMapper;
use Math::Combinatorics;
use  List::Compare;
use Data::Dumper;

# human
use DbHumanGeneName;
use DbHumanGeneProtein;
#use DbHumanSummarySheet;
#mouse
use DbMouseGeneName;
use DbMouseGeneProtein;
#use DbMouseSummarySheet;

#yeast
use DbYeastGeneName;
use DbYeastGeneProtein;
#use DbYeastSummarySheet;

use CGI;

#use Time::HiRes qw { time };

my $q    = new CGI;
my %q = %$q;
my $background = $q->param( "background" );
my $section = $q->param( "section" );
my $position = $q->param("pos");
my $sort_by_field_name = $q->param("sort");
my $asc_or_desc = $q->param("ad");
my $session = $q->param("session");
my $list = $q->param("list");
my $org = $q->param("org");
my $gene = $q->param("gene");
my $proteins = $q->param("proteins");
my $tf = $q->param("tf");
my $gene_name = $q->param("gene_name");
#my $mitocheck_action = $q->param("action"); #mitocheck related

	if(!$background) {
		$background = "";
	}
	if(!$section) {
		$section = "";
	}
	if(!$position) {
		$position = "";
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
	if(!$list) {
		$list = "";
	}
	if(!$org) {
		$org = "";
	}
	if(!$proteins) {
		$proteins = "";
	}
	if(!$tf) {
		$tf = "";
	}
	if(!$gene_name) {
		$gene_name = "";
	}
#	if(!$mitocheck_action) {
#		$mitocheck_action = "";
#	}

my $host_name = "http://biocompendium.embl.de";
#my $URL_project = $host_name . "/biocompendium/";
my $URL_project = $host_name . "/";
my $URL_cgi = $host_name . "/cgi-bin/biocompendium.cgi";
my $STITCH_URL = "http://stitch.embl.de";
my $chemistry_url = $URL_project . "/temp/structure/";
my $pubchem_url = "http://pubchem.ncbi.nlm.nih.gov/summary/summary.cgi?cid=";
my $dasty2das_client = "http://www.ebi.ac.uk/dasty/client/ebi.php";
my $outPutDir = "/usr/local/www_schn/apache22/htdocs/biocompendium/temp/";
my $cgi_dir = "/usr/local/www_schn/apache22/cgi-bin/";
my $biocompendium_perl = $cgi_dir . "biocompendium_perl/";
my $uniprot_uri = "http://uniprot.org/uniprot";
	my $hyper_link_img = "hyperlink.png";
	my $hyper_link_flag_img = "flag.png";
	my $hyper_link_img_width = '12';
	my $hyper_link_img_height = '12';
	my $table_width = '1200';
print $q->header( "text/html" ),
      $q->start_html( -title=>'bioCompendium',
		      -auther=>'Venkata P. Satagopam (venkata.satagopam@embl.de)',
			-meta=> {keywords=>'bioCompendium EMBL Venkata P. Satagopam venkata.satagopam@embl.de'},
			-style=>{-src=>['/style/biocompendium.css', '/style/biocompendium_popup.css']},
			-script=>[
					{-language=>'JAVASCRIPT',
					-src=>'/javascript/overlib.js'},
					{-language=>'JAVASCRIPT',
					-src=>'/javascript/tool_tip.js'},
					{-language=>'JAVASCRIPT',
					-src=>'/javascript/dynamic_file_upload.js'},
					{-language=>'JAVASCRIPT',
					-src=>'/javascript/id_type.js'},
					{-language=>'JAVASCRIPT',
					-src=>'/javascript/prototype.js'},
					{-language=>'JAVASCRIPT',
					-src=>'/javascript/effects.js'},
					{-language=>'JAVASCRIPT',
					-src=>'/javascript/dragdrop.js'},
					{-language=>'JAVASCRIPT',
					-src=>'/javascript/controls.js'},
					{-language=>'JAVASCRIPT',
					-src=>'/javascript/biocompendium.js'},
					{-language=>'JAVASCRIPT',
					-src=>'/javascript/biocompendium_popup.js'},
					{-language=>'JAVASCRIPT',
					-src=>'/javascript/checkboxes.js'},
				],
			-onload=>'return toggleAll(\'collapse\')'
		    );

# this line include the form action, cgi script etc, ...very nice one
	my $form_name = "biocompendium";
	my $method = "POST";
	my $action = "/cgi-bin/biocompendium.cgi";
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

	my %tuples = (
			2 => 'Pairs (Doublets)',
			3 => 'Triples (Triplets)',
			4 => 'Quadruples',
			5 => 'Quintuples (Pentuples)',
			6 => 'Sextuples (Hextuples)',
			7 => 'Septuples',
			8 => 'Octuples',
			9 => 'Nonuples',
			10 => 'Decuples',
			11 => 'Undecuples (Hendecuples)',
			12 => 'Duodecuples',
			13 => '13-Tuples',
			14 => '14-Tuples',
			15 => '15-Tuples',
			16 => '16-Tuples',
			17 => '17-Tuples',
			18 => '18-Tuples',
			19 => '19-Tuples',
			20 => '20-Tuples'
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
	my %orthotype = (
			 'ortholog_one2one' => '<a href="javascript:void(0);" onmouseover="return overlib(\'One2one orthology\', WIDTH, 115);" onmouseout="nd();">one2one</a>',
			 'ortholog_one2many' => '<a href="javascript:void(0);" onmouseover="return overlib(\'One2many orthology\', WIDTH, 125);" onmouseout="nd();">one2many</a>',
			 'ortholog_many2many'  => '<a href="javascript:void(0);" onmouseover="return overlib(\'Many2many orthology\', WIDTH, 130);" onmouseout="nd();">many2many</a>',
			 'apparent_ortholog_one2one' => '<a href="javascript:void(0);" onmouseover="return overlib(\'Apparent one2one orthology\', WIDTH, 165);" onmouseout="nd();">apprent_one2one</a>'				
			);
	my %param_hash = ();
	my %gene_list_name_hash = ();
	my %org_hash = ();
	my %id_doc_type_hash = ();
	my %file_hash = ();
	my %mitocheck_hash = ();
  my %tamahud_hash = ();

	my $no_gene_lists = 0;
	my @nums = ();
	if ($section eq 'upload_gene_lists_tamahud') {
		foreach my $p (keys %q) {
#print "p : $p<br>";
			if ($p =~ /gene_list/) {
				$no_gene_lists++;
				my $value = $q->param("$p");
				my @value =  split("\n", $value);
#print "@value";
#print "value : $value<br>";
#"human" . "____" . $exp . "____ensembl_gene_id____" . $entrez_ids_str;
#				my ($org, $gene_list_name, $id_doc_type, $ids_str) = split("____", $value);
				my $org = shift @value;
				$org=~ s/\r|\n| //g;
				my $gene_list_name = shift @value;
				$gene_list_name=~ s/\r|\n| //g;
				my $id_doc_type = shift @value;
				$id_doc_type=~ s/\r|\n| //g;
#print "org : $org<br>";
#print "gene_list_name : $gene_list_name<br>";
#print "id_doc_type : $id_doc_type<br>";
				my $value_str = join("__", @value);
				$value_str=~ s/\r|\n| //g;
#print "value_str : $value_str<br>";

				$p =~ s/gene_list//;
				$tamahud_hash{$p} = $value_str;
				push @nums, $p;
				my $org_key = 'Category' . $p;
				$org_hash{$org_key} = $org;
				$param_hash{$p}{org} = $org;
				$param_hash{$p}{list_name} = $gene_list_name;
				$param_hash{$p}{id_doc_type} = $id_doc_type;
			} # if ($p =~ /gene_list/) {
		} # foreach my $p (keys %q) {
	}
	elsif ($section eq 'upload_gene_lists') {
		foreach my $p (keys %q) {
			my $gene_list_name = $p;
			if ($p =~ /gene_list/) {
				$no_gene_lists++;
				my $value = $q->param("$p");
				$p =~ s/gene_list//;
#print "value $p: $value";				
				$value =~ s/\r//g;
				$value =~ s/ |\t//g;
				$mitocheck_hash{$p} = $value;
				push @nums, $p;
				my $org_key = 'Category' . $p;
				$org_hash{$org_key} = 'human';
				$param_hash{$p}{org} = 'human';
				$param_hash{$p}{list_name} = $gene_list_name;
				$param_hash{$p}{id_doc_type} = 'list';
			} # if ($p =~ /gene_list/) {
		} # foreach my $p (keys %q) {
	} # if ($section eq "upload_gene_lists") {
	else {
		foreach my $p (keys %q) {
#print "p : $p\n";
			if ($p =~ /gene_list/) {
				$no_gene_lists++;
				my $value = $q->param("$p");
				$gene_list_name_hash{$p} = $value;

				$p =~ s/gene_list_//; 
				push @nums, $p;
				$param_hash{$p}{list_name} = $value;
			} # if ($p =~ /gene_list/) {

			if ($p =~ /Category/) {
				my $value = $q->param("$p");
				$org_hash{$p} = $value;
	
				$p =~ s/Category//;
				$param_hash{$p}{org} = $value;
			} # if ($p =~ /Category/) {

			if ($p =~ /SubCat/) {
				my $value = $q->param("$p");
				$id_doc_type_hash{$p} = $value;

				$p =~ s/SubCat//;
				$param_hash{$p}{id_doc_type} = $value;
			} # if ($p =~ /SubCat/) {

			if ($p =~ /attachment/) {
				my $value = $q->param("$p");
				$file_hash{$p} = $value;

				$p =~ s/attachment//;
				$param_hash{$p}{file} = $value;
			} # if ($p =~ /attachment/) {
		} # foreach my $p (keys %q) {
	} # else {

### this is related to background selection, if the user select 'other gene list(s)' option and provides only one gene list, this is wrong
# selection, in this particular case, he need to take select 'whole genome' as background, the following snippet checks this one
#print "background : $background";
	my $background_selection_check = "yes";
	if (($no_gene_lists ==1) && $background eq "other_gene_lists") {
		$background = "whole_genome";
		$background_selection_check = "no";	
	} # if (($no_gene_lists ==1) && $background eq "other_gene_lists") {
 
	if ($section eq "biodb") {
		&table_view($position, $session, $list, $org, $sort_by_field_name, $asc_or_desc);
	}
	elsif($section eq "summary_sheet") {
		&summary_sheet($gene, $org);
	}
	elsif($section eq "domains") {
		&domain_clustering($position, $session, $list, $org);
	}
	elsif ($section eq "homology_clustering") {
		 &homology_clustering($position, $session, $list, $org);
	}
	elsif ($section eq "orthology") {
		 &orthology($position, $session, $list, $org);
	}
	elsif ($section eq "pathway") {
		 &pathway($position, $session, $list, $org);
	}
	elsif ($section eq "chemistry") {
		 &chemistry($position, $session, $list, $org);
	}
	elsif ($section eq "go") {
		 &go($background, $position, $session, $list, $org);
	}
	elsif ($section eq "transcription_factor") {
		 &transcription_factor($position, $session, $list, $org);
	}
	elsif ($section eq "transcription_factor_details") {
		 &transcription_factor_details($org, $gene, $gene_name, $tf);
	}
	elsif ($section eq "patent") {
		 &patent($position, $session, $list, $org);
	}
	elsif ($section eq "clinical_trials") {
		 &clinical_trials($position, $session, $list, $org);
	}
#	elsif ($section eq "visualization") {
#		 &visualization($position, $session, $list, $org);
#	}
	elsif ($section eq "interaction") {
		 &interaction($position, $session, $list, $org);
	}
	elsif($section eq "graph_view") {
		&graph_view($proteins, "Smart", $org, "domain");
	}
	else {	
		&process_genelists();
	}

#my $hidden_input = $q->param( "hiddenInput" );
	
print $q->endform;
print $q->end_html;

sub process_genelists {
	&get_browse_banner("");	
#print "no_gene_lists : $no_gene_lists\n<br>";

# Inorder to know what is the organism of the frist gene list, once you know this organism, convert other gene lists into first organism type based on orthologs... 
	@nums = sort @nums;  # the numbers can be any order becuase %q is a hash
	my $size = @nums;
#print "nums : @nums\n<br>";
	my $key = "Category" . $nums[0]; # key of the first list organism type
	my $primary_org = $org_hash{$key}; # first list organism
#print "primary_org : $primary_org<br>";

# session directory
	my $session = `date +%Y%m%d%k%M%S%N`;
	$session =~ s/ //g;
	chop($session);
	$session = "tmp_" . $session;
	my $session_dir = $outPutDir . "sessions/" . $session . "/";
	`rm -rf $session_dir; mkdir $session_dir; chmod -R 777 $session_dir`;

# mysql file 
	close(FH_MYSQL);
	my $mysql_file = $session_dir . "/mysql_file.sql"; 
	open(FH_MYSQL, ">$mysql_file");
	print FH_MYSQL "CREATE DATABASE IF NOT EXISTS $session;\n";
	print FH_MYSQL "USE `$session`;\n";

	my $biggest_gene_list_size = 0;
	my @all_genes = ();
	foreach my $num (@nums) {
#print "num : $num<br>";
		my $id_doc_type = $param_hash{$num}{id_doc_type}; # gives id/doc type of the entered file
		my $list_name = $param_hash{$num}{list_name};  
		my $org = $param_hash{$num}{org};  

		my @gene_list = ();
## this section handle mitocheck data
		if (%tamahud_hash) {
			my $id_list = $tamahud_hash{$num};
			my @temp_id_list = split("__", $id_list);
			my @id_list = ();
			foreach my $e (@temp_id_list) {
				$e=~ s/\r|\r| //g;
#print "e:$e:<br>";
				push @id_list, $e;
			}
#			@id_list = &nonRedundantList(\@id_list);
			if ($id_doc_type ne 'ensembl_gene_id' || $org ne 'human') {
#print "org :$org:<br>";
				@gene_list = &IdMapper::get_ensembl_genes($org, \@id_list, $id_doc_type, $primary_org);
			}
			else {
				@gene_list = @id_list;
			}
			@gene_list = &nonRedundantList(\@gene_list);	
		} # if (%tamahud_hash) {
## if section to handle mitocheck data		
		elsif (%mitocheck_hash) {
			my $gene_list = $mitocheck_hash{$num};
#print "gene_list $num: $gene_list";			
			my @temp_gene_list = split("\n", $gene_list);
			foreach my $gene (@temp_gene_list) {
				if (($gene ne "")&&($gene=~/[a-zA-Z0-9-_]+/)) {
					push @gene_list, $gene;
				}
				@gene_list = &nonRedundantList(\@gene_list);	
			} # foreach my $gene (@temp_gene_list) {
		}
		else {
			my $file = $param_hash{$num}{file};
#print "id_doc_type : $id_doc_type, list_name : $list_name, org : $org, file : $file<br>";
			@gene_list = &get_gene_list($org, $file, $id_doc_type, $primary_org, $session_dir);
#print "gene_list : @gene_list<br>";
		}
#print "gene_list : @gene_list<br>";
		push @all_genes, @gene_list;
		my $gene_list_size = @gene_list;
		$param_hash{$num}{gene_list} = \@gene_list;
		$param_hash{$num}{gene_list_size} = $gene_list_size;
		if ($gene_list_size > $biggest_gene_list_size) {
			$biggest_gene_list_size = $gene_list_size;
		} # if ($gene_list_size > $biggest_gene_list_size) {
	} # foreach my $num (@nums) {
	
	@all_genes = &nonRedundantList(\@all_genes);

print "<table cellpadding=\"10\" border=\"0\"  width=$table_width>\n";
	print "<tbody>";
       	my $imgNo = 0;
		
	print "<tr>\n";
	       	print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Legend</b></font></td>\n";
	       	print "<td><br> Click on color bars to explore more knowledge<br><br></td>\n";
       	print "</tr>";

	print "<tr>\n";
		print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"></font></td>\n";
		print "<td><a href=\"#\" onclick=\"return toggleAll(\'expand\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'expand\' onClick=\'changeImage(\"expand\")\'></a> <font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Expand All</b> </font><a href=\"#\" onclick=\"return toggleAll(\'collapse\')\"> <img alt=\"\" src=\"/images/minus.gif\" name=\'collapse\' onClick=\'changeImage(\"collapse\")\'></a> <font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Collapse All</b></font><br><br></td>\n";
	print "</tr>";
	
	print "<tr>\n";
		print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Selected background</b></font></td>\n";
		my $background_str = "";
		if($background eq "whole_genome") {
			$background_str = "Whole genome";
		}
		else {
			$background_str = "Other gene list(s)";
		}

		if ($background_selection_check eq "no") {
			$background_str .= " (In your current data analysis scenario, the background should be 'whole genome', because there is only one gene list)"
		}
		print "<td>$background_str<br></td>";
	print "</tr>\n";

	print "<tr>\n";
		print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Input after convertion</b></font></td>\n";	
		print "<td><br><table border=1 cellspacing=0 >";
			print "<tr><td class=biocompendium_header>#</td><td class=biocompendium_header>Name</td><td class=biocompendium_header>Size</td><td class=biocompendium_header>Organism</td><tr>\n";
	my $i=0;
	foreach my $num (@nums) {
		$i++;
		my $id_doc_type = $param_hash{$num}{id_doc_type}; # gives id/doc type of the entered file
		my $list_name = $param_hash{$num}{list_name};  
		my $org = $param_hash{$num}{org};  
#		my $file = $param_hash{$num}{file};
		my $gene_list = $param_hash{$num}{gene_list};
		my @gene_list = @$gene_list;
		my $gene_list_size = $param_hash{$num}{gene_list_size};

		my $fh = "";
		my $gene_list_str = "";
		my $table_name = "";
		my $create_table_string = "";
		if (@gene_list) {
			### create gene list table
			$table_name = $list_name . "__" . $i;
			$create_table_string = &create_table($table_name, \@gene_list);
			print FH_MYSQL "$create_table_string";

			### create gene list file
	  	$fh = $session_dir . "$table_name";
			close (FH);
			open(FH,">$fh");
			$gene_list_str = join("\n", @gene_list);
			print FH "$gene_list_str\n";
			close (FH);
		} # if (@gene_list) {	

		if ($background eq 'other_gene_lists') {
			### creating gene list background file
			my $lc = List::Compare->new(\@gene_list, \@all_genes);	
			my @background_only = $lc->get_Ronly;
			if (@background_only) {
				$fh = $session_dir . "$table_name" . "__background";
	    	close (FH);
  	  	open(FH,">$fh");
    		$gene_list_str = join("\n", @background_only);
    		print FH "$gene_list_str\n";
    		close (FH);
			} # if (@background_only) {	
		} # if ($background eq 'other_gene_lists') {

		my $spaces = &getSpaces($biggest_gene_list_size, $gene_list_size);
		my $org_info = "";
		if ($org ne $primary_org) {
			$org_info = $org . "->" . $primary_org;
		}
		else {
			$org_info = $primary_org;
		}
			print "<tr><td class=biocompendium>$i</td><td class=biocompendium>$list_name</td><td class=biocompendium align=right>$gene_list_size  <a class=gene_list$i lang=\"JavaScript\" onclick=\"overlib(list_option_text('$background', '$session', '$table_name', '$primary_org'),STICKY,CAPTION,'$list_name',CLOSECLICK,HAUTO,OFFSETY,0);\">$spaces</a></td><td class=biocompendium>$org_info</td><tr>\n";			

	} #  foreach my $num (@nums) {

		print "</table><br></td>";
	print "</tr>";

my %combi_result_hash = ();
my @all_combi = ();
my @background_genes = ();
if ($size > 1) {
	$imgNo++;
	print "<tr>\n";
		print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Combinations</b></font></td>\n";	
		print "<td>";
			print "<table cellspacing='0' width=$table_width>\n";
				print "<tbody>";
					print "<tr>\n";
						print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_combinations\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> Combinations between maximum top 10 sets: </b></font>";
						print "</td>\n";
					print "</tr>\n";
				print "</tbody>";
				print "<tbody class=\"collapse_obj\" id=\"collapse_combinations\">";
					print "<tr>\n";
						print "<td>";
							print "<table border=0>\n";
									print "<tr><td>";
										print "<table border=0 cellspacing=0 width=700>";
											print "<tr><td width='10%' class=biocompendium_header_left>#</td><td width='10%' class=biocompendium_header_left>Combi</td><td  width='40%' class=biocompendium_header_right>Unique only</td><td></td><td width='40%' class=biocompendium_header_left>Intersection</td></tr>";
										print "</table>";
									print "</td></tr>";
			 for (my $j=2; $j<=$size; $j++) {
#					my $tuple = $tuples{$j};
					my @combinations = &getCombinations($size, $j);
					@combinations = sort(@combinations);
#print "combinations : @combinations<br>";
#					my %combinations = %$combinations;
#					my $allComboKeys = $combinations{allComboKeys};
#					my @allComboKeys = @$allComboKeys;
#
#					my $allCombo = $combinations{allCombo};
#					my %allCombo = %$allCombo;
						
								foreach my $combi (@combinations) {
									unshift @all_combi, $combi;
									my @combi = split(";", $combi);
									my $combi_size = scalar(@combi);

									if ($combi_size == 2) {
										if (!$combi_result_hash{$combi}) {
											my $first_element = $combi[0];
											my $second_element = $combi[1];
											
											my $first_num = $nums[$first_element];	
											my $second_num = $nums[$second_element];	
	
											my $first_gene_list = $param_hash{$first_num}{gene_list};
											my $second_gene_list = $param_hash{$second_num}{gene_list};
											
											my $lc = List::Compare->new($first_gene_list, $second_gene_list);
											my @intersection = $lc->get_intersection;
											my @first_only = $lc->get_Lonly;
											my @second_only = $lc->get_Ronly;
						
											if (@intersection) {
												$combi_result_hash{$combi}{i}{gene_list} = \@intersection;  	
												$combi_result_hash{$combi}{$first_element}{gene_list} = \@first_only;
												$combi_result_hash{$combi}{$second_element}{gene_list} = \@second_only;
												if ($background eq 'other_gene_lists') {
													my @intersection_background = (@first_only, @second_only);
													@intersection_background = &nonRedundantList(\@intersection_background);
													$combi_result_hash{$combi}{i}{background_gene_list} = \@intersection_background;  	
													
													my @first_only_background = @second_only;
													$combi_result_hash{$combi}{$first_element}{background_gene_list} = \@first_only_background;

													my @second_only_background = @first_only;
													$combi_result_hash{$combi}{$second_element}{background_gene_list} = \@second_only_background;
												} # if ($background eq 'other_gene_lists') {
											} # f (@intersection) {
										} # if (!$combi_result_hash{$combi}) {
									} # if ($combi_size == 2) {
### combinatin size 3	###								
									elsif ($combi_size == 3) {
										if (!$combi_result_hash{$combi}) {
										my $first_element  = $combi[0];
										my $second_element = $combi[1];
										my $third_element  = $combi[2];
										my $first_second_element = $combi[0] . ";" . $combi[1];

										my $first_num  = $nums[$first_element];
										my $second_num = $nums[$second_element];
										my $third_num  = $nums[$third_element];

                    my $first_gene_list  = $param_hash{$first_num}{gene_list};
										my $second_gene_list = $param_hash{$second_num}{gene_list};										
										my $third_gene_list  = $param_hash{$third_num}{gene_list};

										if ($combi_result_hash{$first_second_element}) {
											my $i = $combi_result_hash{$first_second_element}{i}{gene_list}; 	
											my $lc = List::Compare->new($i, $third_gene_list);
											my @intersection = $lc->get_intersection;

											if (@intersection) {
												my $lc = List::Compare->new($first_gene_list, \@intersection);	
												my @first_only = $lc->get_Lonly;
												$lc = List::Compare->new($second_gene_list, \@intersection);
												my @second_only = $lc->get_Lonly;
												$lc = List::Compare->new($third_gene_list, \@intersection);
												my @third_only = $lc->get_Lonly;
												$combi_result_hash{$combi}{i}{gene_list} = \@intersection;
												$combi_result_hash{$combi}{$first_element}{gene_list}  = \@first_only;
												$combi_result_hash{$combi}{$second_element}{gene_list} = \@second_only;
												$combi_result_hash{$combi}{$third_element}{gene_list}  = \@third_only;
												if ($background eq 'other_gene_lists') {
													my @intersection_background = (@first_only, @second_only, @third_only);
													@intersection_background = &nonRedundantList(\@intersection_background);
													$combi_result_hash{$combi}{i}{background_gene_list} = \@intersection_background;  	
													
													my @first_only_background = (@second_only, @third_only);
													@first_only_background = &nonRedundantList(\@first_only_background);
													$combi_result_hash{$combi}{$first_element}{background_gene_list} = \@first_only_background;

													my @second_only_background = (@first_only, @third_only);
													@second_only_background = &nonRedundantList(\@second_only_background);
													$combi_result_hash{$combi}{$second_element}{background_gene_list} = \@second_only_background;

													my @third_only_background = (@first_only, @second_only);
													@third_only_background = &nonRedundantList(\@third_only_background);
													$combi_result_hash{$combi}{$third_element}{background_gene_list} = \@third_only_background;
												} # if ($background eq 'other_gene_lists') {
											} # if (@intersection) {
										} # if ($combi_result_hash{$first_second_element}) {
										} # if (!$combi_result_hash{$combi}) {
									} # elsif ($combi_size == 3) {
### combinatin size 4	###								
									elsif ($combi_size == 4) {
										if (!$combi_result_hash{$combi}) {
										my $first_element  = $combi[0];
										my $second_element = $combi[1];
										my $third_element  = $combi[2];
										my $fourth_element = $combi[3];
										my $first_second_third_element = $combi[0] . ";" . $combi[1] . ";" . $combi[2];

										my $first_num  = $nums[$first_element];
										my $second_num = $nums[$second_element];
										my $third_num  = $nums[$third_element];
										my $fourth_num = $nums[$fourth_element];

                    my $first_gene_list  = $param_hash{$first_num}{gene_list};
										my $second_gene_list = $param_hash{$second_num}{gene_list};										
										my $third_gene_list  = $param_hash{$third_num}{gene_list};
										my $fourth_gene_list = $param_hash{$fourth_num}{gene_list};

										if ($combi_result_hash{$first_second_third_element}) {
											my $i = $combi_result_hash{$first_second_third_element}{i}{gene_list}; 	
											my $lc = List::Compare->new($i, $fourth_gene_list);
											my @intersection = $lc->get_intersection;

											if (@intersection) {
												my $lc = List::Compare->new($first_gene_list, \@intersection);	
												my @first_only = $lc->get_Lonly;
												$lc = List::Compare->new($second_gene_list, \@intersection);
												my @second_only = $lc->get_Lonly;
												$lc = List::Compare->new($third_gene_list, \@intersection);
												my @third_only = $lc->get_Lonly;
												$lc = List::Compare->new($fourth_gene_list, \@intersection);
												my @fourth_only = $lc->get_Lonly;
												$combi_result_hash{$combi}{i}{gene_list} = \@intersection;
												$combi_result_hash{$combi}{$first_element}{gene_list}  = \@first_only;
												$combi_result_hash{$combi}{$second_element}{gene_list} = \@second_only;
												$combi_result_hash{$combi}{$third_element}{gene_list}  = \@third_only;
												$combi_result_hash{$combi}{$fourth_element}{gene_list} = \@fourth_only;
												if ($background eq 'other_gene_lists') {
													my @intersection_background = (@first_only, @second_only, @third_only, @fourth_only);
													@intersection_background = &nonRedundantList(\@intersection_background);
													$combi_result_hash{$combi}{i}{background_gene_list} = \@intersection_background;  	
													
													my @first_only_background = (@second_only, @third_only, @fourth_only);
													@first_only_background = &nonRedundantList(\@first_only_background);
													$combi_result_hash{$combi}{$first_element}{background_gene_list} = \@first_only_background;

													my @second_only_background = (@first_only, @third_only, @fourth_only);
													@second_only_background = &nonRedundantList(\@second_only_background);
													$combi_result_hash{$combi}{$second_element}{background_gene_list} = \@second_only_background;

													my @third_only_background = (@first_only, @second_only, @fourth_only);
													@third_only_background = &nonRedundantList(\@third_only_background);
													$combi_result_hash{$combi}{$third_element}{background_gene_list} = \@third_only_background;

													my @fourth_only_background = (@first_only, @second_only, @third_only);
													@fourth_only_background = &nonRedundantList(\@fourth_only_background);
													$combi_result_hash{$combi}{$fourth_element}{background_gene_list} = \@fourth_only_background;
												} # if ($background eq 'other_gene_lists') {
											} # if (@intersection) {
										} # if ($combi_result_hash{$first_second_third_element}) {
										} # if (!$combi_result_hash{$combi}) {
									} # elsif ($combi_size == 4) {
### combinatin size 5	###								
									elsif ($combi_size == 5) {
										if (!$combi_result_hash{$combi}) {
										my $first_element  = $combi[0];
										my $second_element = $combi[1];
										my $third_element  = $combi[2];
										my $fourth_element = $combi[3];
										my $fifth_element  = $combi[4];
										my $first_2nd_3rd_4th_element = $combi[0] . ";" . $combi[1] . ";" . $combi[2] . ";" . $combi[3];

										my $first_num  = $nums[$first_element];
										my $second_num = $nums[$second_element];
										my $third_num  = $nums[$third_element];
										my $fourth_num = $nums[$fourth_element];
										my $fifth_num  = $nums[$fifth_element];

                    my $first_gene_list  = $param_hash{$first_num}{gene_list};
										my $second_gene_list = $param_hash{$second_num}{gene_list};										
										my $third_gene_list  = $param_hash{$third_num}{gene_list};
										my $fourth_gene_list = $param_hash{$fourth_num}{gene_list};
										my $fifth_gene_list  = $param_hash{$fifth_num}{gene_list};

										if ($combi_result_hash{$first_2nd_3rd_4th_element}) {
											my $i = $combi_result_hash{$first_2nd_3rd_4th_element}{i}{gene_list}; 	
											my $lc = List::Compare->new($i, $fifth_gene_list);
											my @intersection = $lc->get_intersection;

											if (@intersection) {
												my $lc = List::Compare->new($first_gene_list, \@intersection);	
												my @first_only = $lc->get_Lonly;
												$lc = List::Compare->new($second_gene_list, \@intersection);
												my @second_only = $lc->get_Lonly;
												$lc = List::Compare->new($third_gene_list, \@intersection);
												my @third_only = $lc->get_Lonly;
												$lc = List::Compare->new($fourth_gene_list, \@intersection);
												my @fourth_only = $lc->get_Lonly;
												$lc = List::Compare->new($fifth_gene_list, \@intersection);
												my @fifth_only = $lc->get_Lonly;
												$combi_result_hash{$combi}{i}{gene_list} = \@intersection;
												$combi_result_hash{$combi}{$first_element}{gene_list}  = \@first_only;
												$combi_result_hash{$combi}{$second_element}{gene_list} = \@second_only;
												$combi_result_hash{$combi}{$third_element}{gene_list}  = \@third_only;
												$combi_result_hash{$combi}{$fourth_element}{gene_list} = \@fourth_only;
												$combi_result_hash{$combi}{$fifth_element}{gene_list}  = \@fifth_only;
												if ($background eq 'other_gene_lists') {
													my @intersection_background = (@first_only, @second_only, @third_only, @fourth_only, @fifth_only);
													@intersection_background = &nonRedundantList(\@intersection_background);
													$combi_result_hash{$combi}{i}{background_gene_list} = \@intersection_background;  	
													
													my @first_only_background = (@second_only, @third_only, @fourth_only, @fifth_only);
													@first_only_background = &nonRedundantList(\@first_only_background);
													$combi_result_hash{$combi}{$first_element}{background_gene_list} = \@first_only_background;

													my @second_only_background = (@first_only, @third_only, @fourth_only, @fifth_only);
													@second_only_background = &nonRedundantList(\@second_only_background);
													$combi_result_hash{$combi}{$second_element}{background_gene_list} = \@second_only_background;

													my @third_only_background = (@first_only, @second_only, @fourth_only, @fifth_only);
													@third_only_background = &nonRedundantList(\@third_only_background);
													$combi_result_hash{$combi}{$third_element}{background_gene_list} = \@third_only_background;

													my @fourth_only_background = (@first_only, @second_only, @third_only, @fifth_only);
													@fourth_only_background = &nonRedundantList(\@fourth_only_background);
													$combi_result_hash{$combi}{$fourth_element}{background_gene_list} = \@fourth_only_background;

													my @fifth_only_background = (@first_only, @second_only, @third_only, @fourth_only);
													@fifth_only_background = &nonRedundantList(\@fifth_only_background);
													$combi_result_hash{$combi}{$fifth_element}{background_gene_list} = \@fifth_only_background;
												} # if ($background eq 'other_gene_lists') {
											} # if (@intersection) {
										} # if ($combi_result_hash{$first_second_third_element}) {
										} # if (!$combi_result_hash{$combi}) {
									} # elsif ($combi_size == 5) {
### combinatin size 6	###								
									elsif ($combi_size == 6) {
										if (!$combi_result_hash{$combi}) {
										my $first_element  = $combi[0];
										my $second_element = $combi[1];
										my $third_element  = $combi[2];
										my $fourth_element = $combi[3];
										my $fifth_element  = $combi[4];
										my $sixth_element  = $combi[5];
										my $first_2nd_3rd_4th_5th_element = $combi[0] . ";" . $combi[1] . ";" . $combi[2] . ";" . $combi[3] . ";" . $combi[4];

										my $first_num  = $nums[$first_element];
										my $second_num = $nums[$second_element];
										my $third_num  = $nums[$third_element];
										my $fourth_num = $nums[$fourth_element];
										my $fifth_num  = $nums[$fifth_element];
										my $sixth_num  = $nums[$sixth_element];

                    my $first_gene_list  = $param_hash{$first_num}{gene_list};
										my $second_gene_list = $param_hash{$second_num}{gene_list};										
										my $third_gene_list  = $param_hash{$third_num}{gene_list};
										my $fourth_gene_list = $param_hash{$fourth_num}{gene_list};
										my $fifth_gene_list  = $param_hash{$fifth_num}{gene_list};
										my $sixth_gene_list  = $param_hash{$sixth_num}{gene_list};

										if ($combi_result_hash{$first_2nd_3rd_4th_5th_element}) {
											my $i = $combi_result_hash{$first_2nd_3rd_4th_5th_element}{i}{gene_list}; 	
											my $lc = List::Compare->new($i, $sixth_gene_list);
											my @intersection = $lc->get_intersection;

											if (@intersection) {
												my $lc = List::Compare->new($first_gene_list, \@intersection);	
												my @first_only = $lc->get_Lonly;
												$lc = List::Compare->new($second_gene_list, \@intersection);
												my @second_only = $lc->get_Lonly;
												$lc = List::Compare->new($third_gene_list, \@intersection);
												my @third_only = $lc->get_Lonly;
												$lc = List::Compare->new($fourth_gene_list, \@intersection);
												my @fourth_only = $lc->get_Lonly;
												$lc = List::Compare->new($fifth_gene_list, \@intersection);
												my @fifth_only = $lc->get_Lonly;
												$lc = List::Compare->new($sixth_gene_list, \@intersection);
												my @sixth_only = $lc->get_Lonly;
												$combi_result_hash{$combi}{i}{gene_list} = \@intersection;
												$combi_result_hash{$combi}{$first_element}{gene_list}  = \@first_only;
												$combi_result_hash{$combi}{$second_element}{gene_list} = \@second_only;
												$combi_result_hash{$combi}{$third_element}{gene_list}  = \@third_only;
												$combi_result_hash{$combi}{$fourth_element}{gene_list} = \@fourth_only;
												$combi_result_hash{$combi}{$fifth_element}{gene_list}  = \@fifth_only;
												$combi_result_hash{$combi}{$sixth_element}{gene_list}  = \@sixth_only;
												if ($background eq 'other_gene_lists') {
													my @intersection_background = (@first_only, @second_only, @third_only, @fourth_only, @fifth_only, @sixth_only);
													@intersection_background = &nonRedundantList(\@intersection_background);
													$combi_result_hash{$combi}{i}{background_gene_list} = \@intersection_background;  	
													
													my @first_only_background = (@second_only, @third_only, @fourth_only, @fifth_only, @sixth_only);
													@first_only_background = &nonRedundantList(\@first_only_background);
													$combi_result_hash{$combi}{$first_element}{background_gene_list} = \@first_only_background;

													my @second_only_background = (@first_only, @third_only, @fourth_only, @fifth_only, @sixth_only);
													@second_only_background = &nonRedundantList(\@second_only_background);
													$combi_result_hash{$combi}{$second_element}{background_gene_list} = \@second_only_background;

													my @third_only_background = (@first_only, @second_only, @fourth_only, @fifth_only, @sixth_only);
													@third_only_background = &nonRedundantList(\@third_only_background);
													$combi_result_hash{$combi}{$third_element}{background_gene_list} = \@third_only_background;

													my @fourth_only_background = (@first_only, @second_only, @third_only, @fifth_only, @sixth_only);
													@fourth_only_background = &nonRedundantList(\@fourth_only_background);
													$combi_result_hash{$combi}{$fourth_element}{background_gene_list} = \@fourth_only_background;

													my @fifth_only_background = (@first_only, @second_only, @third_only, @fourth_only, @sixth_only);
													@fifth_only_background = &nonRedundantList(\@fifth_only_background);
													$combi_result_hash{$combi}{$fifth_element}{background_gene_list} = \@fifth_only_background;

													my @sixth_only_background = (@first_only, @second_only, @third_only, @fourth_only, @fifth_only);
													@sixth_only_background = &nonRedundantList(\@sixth_only_background);
													$combi_result_hash{$combi}{$sixth_element}{background_gene_list} = \@sixth_only_background;
												} # if ($background eq 'other_gene_lists') {
											} # if (@intersection) {
										} # if ($combi_result_hash{$first_second_third_element}) {
										} # if (!$combi_result_hash{$combi}) {
									} # elsif ($combi_size == 6) {
### combinatin size 7	###								
									elsif ($combi_size == 7) {
										if (!$combi_result_hash{$combi}) {
										my $first_element   = $combi[0];
										my $second_element  = $combi[1];
										my $third_element   = $combi[2];
										my $fourth_element  = $combi[3];
										my $fifth_element   = $combi[4];
										my $sixth_element   = $combi[5];
										my $seventh_element = $combi[6];
										my $first_2nd_3rd_4th_5th_6th_element = $combi[0] . ";" . $combi[1] . ";" . $combi[2] . ";" . $combi[3] . ";" . $combi[4] . ";" . $combi[5];

										my $first_num   = $nums[$first_element];
										my $second_num  = $nums[$second_element];
										my $third_num   = $nums[$third_element];
										my $fourth_num  = $nums[$fourth_element];
										my $fifth_num   = $nums[$fifth_element];
										my $sixth_num   = $nums[$sixth_element];
										my $seventh_num = $nums[$seventh_element];

                    my $first_gene_list   = $param_hash{$first_num}{gene_list};
										my $second_gene_list  = $param_hash{$second_num}{gene_list};										
										my $third_gene_list   = $param_hash{$third_num}{gene_list};
										my $fourth_gene_list  = $param_hash{$fourth_num}{gene_list};
										my $fifth_gene_list   = $param_hash{$fifth_num}{gene_list};
										my $sixth_gene_list   = $param_hash{$sixth_num}{gene_list};
										my $seventh_gene_list = $param_hash{$seventh_num}{gene_list};

										if ($combi_result_hash{$first_2nd_3rd_4th_5th_6th_element}) {
											my $i = $combi_result_hash{$first_2nd_3rd_4th_5th_6th_element}{i}{gene_list}; 	
											my $lc = List::Compare->new($i, $seventh_gene_list);
											my @intersection = $lc->get_intersection;

											if (@intersection) {
												my $lc = List::Compare->new($first_gene_list, \@intersection);	
												my @first_only = $lc->get_Lonly;
												$lc = List::Compare->new($second_gene_list, \@intersection);
												my @second_only = $lc->get_Lonly;
												$lc = List::Compare->new($third_gene_list, \@intersection);
												my @third_only = $lc->get_Lonly;
												$lc = List::Compare->new($fourth_gene_list, \@intersection);
												my @fourth_only = $lc->get_Lonly;
												$lc = List::Compare->new($fifth_gene_list, \@intersection);
												my @fifth_only = $lc->get_Lonly;
												$lc = List::Compare->new($sixth_gene_list, \@intersection);
												my @sixth_only = $lc->get_Lonly;
												$lc = List::Compare->new($seventh_gene_list, \@intersection);
												my @seventh_only = $lc->get_Lonly;
												$combi_result_hash{$combi}{i}{gene_list} = \@intersection;
												$combi_result_hash{$combi}{$first_element}{gene_list}   = \@first_only;
												$combi_result_hash{$combi}{$second_element}{gene_list}  = \@second_only;
												$combi_result_hash{$combi}{$third_element}{gene_list}   = \@third_only;
												$combi_result_hash{$combi}{$fourth_element}{gene_list}  = \@fourth_only;
												$combi_result_hash{$combi}{$fifth_element}{gene_list}   = \@fifth_only;
												$combi_result_hash{$combi}{$sixth_element}{gene_list}   = \@sixth_only;
												$combi_result_hash{$combi}{$seventh_element}{gene_list} = \@seventh_only;
												if ($background eq 'other_gene_lists') {
													my @intersection_background = (@first_only, @second_only, @third_only, @fourth_only, @fifth_only, @sixth_only, @seventh_only);
													@intersection_background = &nonRedundantList(\@intersection_background);
													$combi_result_hash{$combi}{i}{background_gene_list} = \@intersection_background;  	
													
													my @first_only_background = (@second_only, @third_only, @fourth_only, @fifth_only, @sixth_only, @seventh_only);
													@first_only_background = &nonRedundantList(\@first_only_background);
													$combi_result_hash{$combi}{$first_element}{background_gene_list} = \@first_only_background;

													my @second_only_background = (@first_only, @third_only, @fourth_only, @fifth_only, @sixth_only, @seventh_only);
													@second_only_background = &nonRedundantList(\@second_only_background);
													$combi_result_hash{$combi}{$second_element}{background_gene_list} = \@second_only_background;

													my @third_only_background = (@first_only, @second_only, @fourth_only, @fifth_only, @sixth_only, @seventh_only);
													@third_only_background = &nonRedundantList(\@third_only_background);
													$combi_result_hash{$combi}{$third_element}{background_gene_list} = \@third_only_background;

													my @fourth_only_background = (@first_only, @second_only, @third_only, @fifth_only, @sixth_only, @seventh_only);
													@fourth_only_background = &nonRedundantList(\@fourth_only_background);
													$combi_result_hash{$combi}{$fourth_element}{background_gene_list} = \@fourth_only_background;

													my @fifth_only_background = (@first_only, @second_only, @third_only, @fourth_only, @sixth_only, @seventh_only);
													@fifth_only_background = &nonRedundantList(\@fifth_only_background);
													$combi_result_hash{$combi}{$fifth_element}{background_gene_list} = \@fifth_only_background;

													my @sixth_only_background = (@first_only, @second_only, @third_only, @fourth_only, @fifth_only, @seventh_only);
													@sixth_only_background = &nonRedundantList(\@sixth_only_background);
													$combi_result_hash{$combi}{$sixth_element}{background_gene_list} = \@sixth_only_background;

													my @seventh_only_background = (@first_only, @second_only, @third_only, @fourth_only, @fifth_only, @sixth_only);
													@seventh_only_background = &nonRedundantList(\@seventh_only_background);
													$combi_result_hash{$combi}{$seventh_element}{background_gene_list} = \@seventh_only_background;
												} # if ($background eq 'other_gene_lists') {
											} # if (@intersection) {
										} # if ($combi_result_hash{$first_second_third_element}) @
										} # if (!$combi_result_hash{$combi}) {
									} # elsif ($combi_size == 7) {
### combinatin size 8	###								
									elsif ($combi_size == 8) {
										if (!$combi_result_hash{$combi}) {
										my $first_element   = $combi[0];
										my $second_element  = $combi[1];
										my $third_element   = $combi[2];
										my $fourth_element  = $combi[3];
										my $fifth_element   = $combi[4];
										my $sixth_element   = $combi[5];
										my $seventh_element = $combi[6];
										my $eighth_element  = $combi[7];
										my $first_2nd_3rd_4th_5th_6th_7th_element = $combi[0] . ";" . $combi[1] . ";" . $combi[2] . ";" . $combi[3] . ";" . $combi[4] . ";" . $combi[5] . ";" . $combi[6];

										my $first_num   = $nums[$first_element];
										my $second_num  = $nums[$second_element];
										my $third_num   = $nums[$third_element];
										my $fourth_num  = $nums[$fourth_element];
										my $fifth_num   = $nums[$fifth_element];
										my $sixth_num   = $nums[$sixth_element];
										my $seventh_num = $nums[$seventh_element];
										my $eighth_num  = $nums[$eighth_element];

                    my $first_gene_list   = $param_hash{$first_num}{gene_list};
										my $second_gene_list  = $param_hash{$second_num}{gene_list};										
										my $third_gene_list   = $param_hash{$third_num}{gene_list};
										my $fourth_gene_list  = $param_hash{$fourth_num}{gene_list};
										my $fifth_gene_list   = $param_hash{$fifth_num}{gene_list};
										my $sixth_gene_list   = $param_hash{$sixth_num}{gene_list};
										my $seventh_gene_list = $param_hash{$seventh_num}{gene_list};
										my $eighth_gene_list  = $param_hash{$eighth_num}{gene_list};

										if ($combi_result_hash{$first_2nd_3rd_4th_5th_6th_7th_element}) {
											my $i = $combi_result_hash{$first_2nd_3rd_4th_5th_6th_7th_element}{i}{gene_list}; 	
											my $lc = List::Compare->new($i, $eighth_gene_list);
											my @intersection = $lc->get_intersection;

											if (@intersection) {
												my $lc = List::Compare->new($first_gene_list, \@intersection);	
												my @first_only = $lc->get_Lonly;
												$lc = List::Compare->new($second_gene_list, \@intersection);
												my @second_only = $lc->get_Lonly;
												$lc = List::Compare->new($third_gene_list, \@intersection);
												my @third_only = $lc->get_Lonly;
												$lc = List::Compare->new($fourth_gene_list, \@intersection);
												my @fourth_only = $lc->get_Lonly;
												$lc = List::Compare->new($fifth_gene_list, \@intersection);
												my @fifth_only = $lc->get_Lonly;
												$lc = List::Compare->new($sixth_gene_list, \@intersection);
												my @sixth_only = $lc->get_Lonly;
												$lc = List::Compare->new($seventh_gene_list, \@intersection);
												my @seventh_only = $lc->get_Lonly;
												$lc = List::Compare->new($eighth_gene_list, \@intersection);
												my @eighth_only = $lc->get_Lonly;
												$combi_result_hash{$combi}{i}{gene_list} = \@intersection;
												$combi_result_hash{$combi}{$first_element}{gene_list}   = \@first_only;
												$combi_result_hash{$combi}{$second_element}{gene_list}  = \@second_only;
												$combi_result_hash{$combi}{$third_element}{gene_list}   = \@third_only;
												$combi_result_hash{$combi}{$fourth_element}{gene_list}  = \@fourth_only;
												$combi_result_hash{$combi}{$fifth_element}{gene_list}   = \@fifth_only;
												$combi_result_hash{$combi}{$sixth_element}{gene_list}   = \@sixth_only;
												$combi_result_hash{$combi}{$seventh_element}{gene_list} = \@seventh_only;
												$combi_result_hash{$combi}{$eighth_element}{gene_list}  = \@eighth_only;
												if ($background eq 'other_gene_lists') {
													my @intersection_background = (@first_only, @second_only, @third_only, @fourth_only, @fifth_only, @sixth_only, @seventh_only, @eighth_only);
													@intersection_background = &nonRedundantList(\@intersection_background);
													$combi_result_hash{$combi}{i}{background_gene_list} = \@intersection_background;  	
													
													my @first_only_background = (@second_only, @third_only, @fourth_only, @fifth_only, @sixth_only, @seventh_only, @eighth_only);
													@first_only_background = &nonRedundantList(\@first_only_background);
													$combi_result_hash{$combi}{$first_element}{background_gene_list} = \@first_only_background;

													my @second_only_background = (@first_only, @third_only, @fourth_only, @fifth_only, @sixth_only, @seventh_only, @eighth_only);
													@second_only_background = &nonRedundantList(\@second_only_background);
													$combi_result_hash{$combi}{$second_element}{background_gene_list} = \@second_only_background;

													my @third_only_background = (@first_only, @second_only, @fourth_only, @fifth_only, @sixth_only, @seventh_only, @eighth_only);
													@third_only_background = &nonRedundantList(\@third_only_background);
													$combi_result_hash{$combi}{$third_element}{background_gene_list} = \@third_only_background;

													my @fourth_only_background = (@first_only, @second_only, @third_only, @fifth_only, @sixth_only, @seventh_only, @eighth_only);
													@fourth_only_background = &nonRedundantList(\@fourth_only_background);
													$combi_result_hash{$combi}{$fourth_element}{background_gene_list} = \@fourth_only_background;

													my @fifth_only_background = (@first_only, @second_only, @third_only, @fourth_only, @sixth_only, @seventh_only, @eighth_only);
													@fifth_only_background = &nonRedundantList(\@fifth_only_background);
													$combi_result_hash{$combi}{$fifth_element}{background_gene_list} = \@fifth_only_background;

													my @sixth_only_background = (@first_only, @second_only, @third_only, @fourth_only, @fifth_only, @seventh_only, @eighth_only);
													@sixth_only_background = &nonRedundantList(\@sixth_only_background);
													$combi_result_hash{$combi}{$sixth_element}{background_gene_list} = \@sixth_only_background;

													my @seventh_only_background = (@first_only, @second_only, @third_only, @fourth_only, @fifth_only, @sixth_only, @eighth_only);
													@seventh_only_background = &nonRedundantList(\@seventh_only_background);
													$combi_result_hash{$combi}{$seventh_element}{background_gene_list} = \@seventh_only_background;

													my @eighth_only_background = (@first_only, @second_only, @third_only, @fourth_only, @fifth_only, @sixth_only, @seventh_only);
													@eighth_only_background = &nonRedundantList(\@eighth_only_background);
													$combi_result_hash{$combi}{$eighth_element}{background_gene_list} = \@eighth_only_background;
												} # if ($background eq 'other_gene_lists') {
											} # if (@intersection) {
										} # if ($combi_result_hash{$first_2nd_3rd_4th_5th_6th_7th_element}) {
										} # if (!$combi_result_hash{$combi}) {
									} # elsif ($combi_size == 8) {
### combinatin size 9	###								
									elsif ($combi_size == 9) {
										if (!$combi_result_hash{$combi}) {
										my $first_element   = $combi[0];
										my $second_element  = $combi[1];
										my $third_element   = $combi[2];
										my $fourth_element  = $combi[3];
										my $fifth_element   = $combi[4];
										my $sixth_element   = $combi[5];
										my $seventh_element = $combi[6];
										my $eighth_element  = $combi[7];
										my $nineth_element  = $combi[8];
										my $first_2nd_3rd_4th_5th_6th_7th_8th_element = $combi[0] . ";" . $combi[1] . ";" . $combi[2] . ";" . $combi[3] . ";" . $combi[4] . ";" . $combi[5] . ";" . $combi[6] . ";" . $combi[7];

										my $first_num   = $nums[$first_element];
										my $second_num  = $nums[$second_element];
										my $third_num   = $nums[$third_element];
										my $fourth_num  = $nums[$fourth_element];
										my $fifth_num   = $nums[$fifth_element];
										my $sixth_num   = $nums[$sixth_element];
										my $seventh_num = $nums[$seventh_element];
										my $eighth_num  = $nums[$eighth_element];
										my $nineth_num  = $nums[$nineth_element];

                    my $first_gene_list   = $param_hash{$first_num}{gene_list};
										my $second_gene_list  = $param_hash{$second_num}{gene_list};										
										my $third_gene_list   = $param_hash{$third_num}{gene_list};
										my $fourth_gene_list  = $param_hash{$fourth_num}{gene_list};
										my $fifth_gene_list   = $param_hash{$fifth_num}{gene_list};
										my $sixth_gene_list   = $param_hash{$sixth_num}{gene_list};
										my $seventh_gene_list = $param_hash{$seventh_num}{gene_list};
										my $eighth_gene_list  = $param_hash{$eighth_num}{gene_list};
										my $nineth_gene_list  = $param_hash{$nineth_num}{gene_list};

										if ($combi_result_hash{$first_2nd_3rd_4th_5th_6th_7th_8th_element}) {
											my $i = $combi_result_hash{$first_2nd_3rd_4th_5th_6th_7th_8th_element}{i}{gene_list}; 	
											my $lc = List::Compare->new($i, $nineth_gene_list);
											my @intersection = $lc->get_intersection;

											if (@intersection) {
												my $lc = List::Compare->new($first_gene_list, \@intersection);	
												my @first_only = $lc->get_Lonly;
												$lc = List::Compare->new($second_gene_list, \@intersection);
												my @second_only = $lc->get_Lonly;
												$lc = List::Compare->new($third_gene_list, \@intersection);
												my @third_only = $lc->get_Lonly;
												$lc = List::Compare->new($fourth_gene_list, \@intersection);
												my @fourth_only = $lc->get_Lonly;
												$lc = List::Compare->new($fifth_gene_list, \@intersection);
												my @fifth_only = $lc->get_Lonly;
												$lc = List::Compare->new($sixth_gene_list, \@intersection);
												my @sixth_only = $lc->get_Lonly;
												$lc = List::Compare->new($seventh_gene_list, \@intersection);
												my @seventh_only = $lc->get_Lonly;
												$lc = List::Compare->new($eighth_gene_list, \@intersection);
												my @eighth_only = $lc->get_Lonly;
												$lc = List::Compare->new($nineth_gene_list, \@intersection);
												my @nineth_only = $lc->get_Lonly;
												$combi_result_hash{$combi}{i}{gene_list} = \@intersection;
												$combi_result_hash{$combi}{$first_element}{gene_list}   = \@first_only;
												$combi_result_hash{$combi}{$second_element}{gene_list}  = \@second_only;
												$combi_result_hash{$combi}{$third_element}{gene_list}   = \@third_only;
												$combi_result_hash{$combi}{$fourth_element}{gene_list}  = \@fourth_only;
												$combi_result_hash{$combi}{$fifth_element}{gene_list}   = \@fifth_only;
												$combi_result_hash{$combi}{$sixth_element}{gene_list}   = \@sixth_only;
												$combi_result_hash{$combi}{$seventh_element}{gene_list} = \@seventh_only;
												$combi_result_hash{$combi}{$eighth_element}{gene_list}  = \@eighth_only;
												$combi_result_hash{$combi}{$nineth_element}{gene_list}  = \@nineth_only;
												if ($background eq 'other_gene_lists') {
													my @intersection_background = (@first_only, @second_only, @third_only, @fourth_only, @fifth_only, @sixth_only, @seventh_only, @eighth_only, @nineth_only);
													@intersection_background = &nonRedundantList(\@intersection_background);
													$combi_result_hash{$combi}{i}{background_gene_list} = \@intersection_background;  	
													
													my @first_only_background = (@second_only, @third_only, @fourth_only, @fifth_only, @sixth_only, @seventh_only, @eighth_only, @nineth_only);
													@first_only_background = &nonRedundantList(\@first_only_background);
													$combi_result_hash{$combi}{$first_element}{background_gene_list} = \@first_only_background;

													my @second_only_background = (@first_only, @third_only, @fourth_only, @fifth_only, @sixth_only, @seventh_only, @eighth_only, @nineth_only);
													@second_only_background = &nonRedundantList(\@second_only_background);
													$combi_result_hash{$combi}{$second_element}{background_gene_list} = \@second_only_background;

													my @third_only_background = (@first_only, @second_only, @fourth_only, @fifth_only, @sixth_only, @seventh_only, @eighth_only, @nineth_only);
													@third_only_background = &nonRedundantList(\@third_only_background);
													$combi_result_hash{$combi}{$third_element}{background_gene_list} = \@third_only_background;

													my @fourth_only_background = (@first_only, @second_only, @third_only, @fifth_only, @sixth_only, @seventh_only, @eighth_only, @nineth_only);
													@fourth_only_background = &nonRedundantList(\@fourth_only_background);
													$combi_result_hash{$combi}{$fourth_element}{background_gene_list} = \@fourth_only_background;

													my @fifth_only_background = (@first_only, @second_only, @third_only, @fourth_only, @sixth_only, @seventh_only, @eighth_only, @nineth_only);
													@fifth_only_background = &nonRedundantList(\@fifth_only_background);
													$combi_result_hash{$combi}{$fifth_element}{background_gene_list} = \@fifth_only_background;

													my @sixth_only_background = (@first_only, @second_only, @third_only, @fourth_only, @fifth_only, @seventh_only, @eighth_only, @nineth_only);
													@sixth_only_background = &nonRedundantList(\@sixth_only_background);
													$combi_result_hash{$combi}{$sixth_element}{background_gene_list} = \@sixth_only_background;

													my @seventh_only_background = (@first_only, @second_only, @third_only, @fourth_only, @fifth_only, @sixth_only, @eighth_only, @nineth_only);
													@seventh_only_background = &nonRedundantList(\@seventh_only_background);
													$combi_result_hash{$combi}{$seventh_element}{background_gene_list} = \@seventh_only_background;

													my @eighth_only_background = (@first_only, @second_only, @third_only, @fourth_only, @fifth_only, @sixth_only, @seventh_only, @nineth_only);
													@eighth_only_background = &nonRedundantList(\@eighth_only_background);
													$combi_result_hash{$combi}{$eighth_element}{background_gene_list} = \@eighth_only_background;

													my @nineth_only_background = (@first_only, @second_only, @third_only, @fourth_only, @fifth_only, @sixth_only, @seventh_only, @eighth_only);
													@nineth_only_background = &nonRedundantList(\@nineth_only_background);
													$combi_result_hash{$combi}{$nineth_element}{background_gene_list} = \@nineth_only_background;
												} # if ($background eq 'other_gene_lists') {
											} # if (@intersection) {
										} # if ($combi_result_hash{$first_2nd_3rd_4th_5th_6th_7th_element}) {
										} # if (!$combi_result_hash{$combi}) {
									} # elsif ($combi_size == 9) {
### combinatin size 10	###								
									elsif ($combi_size == 10) {
										if (!$combi_result_hash{$combi}) {
										my $first_element   = $combi[0];
										my $second_element  = $combi[1];
										my $third_element   = $combi[2];
										my $fourth_element  = $combi[3];
										my $fifth_element   = $combi[4];
										my $sixth_element   = $combi[5];
										my $seventh_element = $combi[6];
										my $eighth_element  = $combi[7];
										my $nineth_element  = $combi[8];
										my $tenth_element   = $combi[9];
										my $first_2nd_3rd_4th_5th_6th_7th_8th_9th_element = $combi[0] . ";" . $combi[1] . ";" . $combi[2] . ";" . $combi[3] . ";" . $combi[4] . ";" . $combi[5] . ";" . $combi[6] . ";" . $combi[7] . ";" . $combi[9];

										my $first_num   = $nums[$first_element];
										my $second_num  = $nums[$second_element];
										my $third_num   = $nums[$third_element];
										my $fourth_num  = $nums[$fourth_element];
										my $fifth_num   = $nums[$fifth_element];
										my $sixth_num   = $nums[$sixth_element];
										my $seventh_num = $nums[$seventh_element];
										my $eighth_num  = $nums[$eighth_element];
										my $nineth_num  = $nums[$nineth_element];
										my $tenth_num   = $nums[$tenth_element];

                    my $first_gene_list   = $param_hash{$first_num}{gene_list};
										my $second_gene_list  = $param_hash{$second_num}{gene_list};										
										my $third_gene_list   = $param_hash{$third_num}{gene_list};
										my $fourth_gene_list  = $param_hash{$fourth_num}{gene_list};
										my $fifth_gene_list   = $param_hash{$fifth_num}{gene_list};
										my $sixth_gene_list   = $param_hash{$sixth_num}{gene_list};
										my $seventh_gene_list = $param_hash{$seventh_num}{gene_list};
										my $eighth_gene_list  = $param_hash{$eighth_num}{gene_list};
										my $nineth_gene_list  = $param_hash{$nineth_num}{gene_list};
										my $tenth_gene_list   = $param_hash{$tenth_num}{gene_list};

										if ($combi_result_hash{$first_2nd_3rd_4th_5th_6th_7th_8th_9th_element}) {
											my $i = $combi_result_hash{$first_2nd_3rd_4th_5th_6th_7th_8th_9th_element}{i}{gene_list}; 	
											my $lc = List::Compare->new($i, $tenth_gene_list);
											my @intersection = $lc->get_intersection;

											if (@intersection) {
												my $lc = List::Compare->new($first_gene_list, \@intersection);	
												my @first_only = $lc->get_Lonly;
												$lc = List::Compare->new($second_gene_list, \@intersection);
												my @second_only = $lc->get_Lonly;
												$lc = List::Compare->new($third_gene_list, \@intersection);
												my @third_only = $lc->get_Lonly;
												$lc = List::Compare->new($fourth_gene_list, \@intersection);
												my @fourth_only = $lc->get_Lonly;
												$lc = List::Compare->new($fifth_gene_list, \@intersection);
												my @fifth_only = $lc->get_Lonly;
												$lc = List::Compare->new($sixth_gene_list, \@intersection);
												my @sixth_only = $lc->get_Lonly;
												$lc = List::Compare->new($seventh_gene_list, \@intersection);
												my @seventh_only = $lc->get_Lonly;
												$lc = List::Compare->new($eighth_gene_list, \@intersection);
												my @eighth_only = $lc->get_Lonly;
												$lc = List::Compare->new($nineth_gene_list, \@intersection);
												my @nineth_only = $lc->get_Lonly;
												$lc = List::Compare->new($tenth_gene_list, \@intersection);
												my @tenth_only = $lc->get_Lonly;
												$combi_result_hash{$combi}{i}{gene_list} = \@intersection;
												$combi_result_hash{$combi}{$first_element}{gene_list}   = \@first_only;
												$combi_result_hash{$combi}{$second_element}{gene_list}  = \@second_only;
												$combi_result_hash{$combi}{$third_element}{gene_list}   = \@third_only;
												$combi_result_hash{$combi}{$fourth_element}{gene_list}  = \@fourth_only;
												$combi_result_hash{$combi}{$fifth_element}{gene_list}   = \@fifth_only;
												$combi_result_hash{$combi}{$sixth_element}{gene_list}   = \@sixth_only;
												$combi_result_hash{$combi}{$seventh_element}{gene_list} = \@seventh_only;
												$combi_result_hash{$combi}{$eighth_element}{gene_list}  = \@eighth_only;
												$combi_result_hash{$combi}{$nineth_element}{gene_list}  = \@nineth_only;
												$combi_result_hash{$combi}{$tenth_element}{gene_list}   = \@tenth_only;
												if ($background eq 'other_gene_lists') {
													my @intersection_background = (@first_only, @second_only, @third_only, @fourth_only, @fifth_only, @sixth_only, @seventh_only, @eighth_only, @nineth_only, @tenth_only);
													@intersection_background = &nonRedundantList(\@intersection_background);
													$combi_result_hash{$combi}{i}{background_gene_list} = \@intersection_background;  	
													
													my @first_only_background = (@second_only, @third_only, @fourth_only, @fifth_only, @sixth_only, @seventh_only, @eighth_only, @nineth_only, @tenth_only);
													@first_only_background = &nonRedundantList(\@first_only_background);
													$combi_result_hash{$combi}{$first_element}{background_gene_list} = \@first_only_background;

													my @second_only_background = (@first_only, @third_only, @fourth_only, @fifth_only, @sixth_only, @seventh_only, @eighth_only, @nineth_only, @tenth_only);
													@second_only_background = &nonRedundantList(\@second_only_background);
													$combi_result_hash{$combi}{$second_element}{background_gene_list} = \@second_only_background;

													my @third_only_background = (@first_only, @second_only, @fourth_only, @fifth_only, @sixth_only, @seventh_only, @eighth_only, @nineth_only, @tenth_only);
													@third_only_background = &nonRedundantList(\@third_only_background);
													$combi_result_hash{$combi}{$third_element}{background_gene_list} = \@third_only_background;

													my @fourth_only_background = (@first_only, @second_only, @third_only, @fifth_only, @sixth_only, @seventh_only, @eighth_only, @nineth_only, @tenth_only);
													@fourth_only_background = &nonRedundantList(\@fourth_only_background);
													$combi_result_hash{$combi}{$fourth_element}{background_gene_list} = \@fourth_only_background;

													my @fifth_only_background = (@first_only, @second_only, @third_only, @fourth_only, @sixth_only, @seventh_only, @eighth_only, @nineth_only, @tenth_only);
													@fifth_only_background = &nonRedundantList(\@fifth_only_background);
													$combi_result_hash{$combi}{$fifth_element}{background_gene_list} = \@fifth_only_background;

													my @sixth_only_background = (@first_only, @second_only, @third_only, @fourth_only, @fifth_only, @seventh_only, @eighth_only, @nineth_only, @tenth_only);
													@sixth_only_background = &nonRedundantList(\@sixth_only_background);
													$combi_result_hash{$combi}{$sixth_element}{background_gene_list} = \@sixth_only_background;

													my @seventh_only_background = (@first_only, @second_only, @third_only, @fourth_only, @fifth_only, @sixth_only, @eighth_only, @nineth_only, @tenth_only);
													@seventh_only_background = &nonRedundantList(\@seventh_only_background);
													$combi_result_hash{$combi}{$seventh_element}{background_gene_list} = \@seventh_only_background;

													my @eighth_only_background = (@first_only, @second_only, @third_only, @fourth_only, @fifth_only, @sixth_only, @seventh_only, @nineth_only, @tenth_only);
													@eighth_only_background = &nonRedundantList(\@eighth_only_background);
													$combi_result_hash{$combi}{$eighth_element}{background_gene_list} = \@eighth_only_background;

													my @nineth_only_background = (@first_only, @second_only, @third_only, @fourth_only, @fifth_only, @sixth_only, @seventh_only, @eighth_only, @tenth_only);
													@nineth_only_background = &nonRedundantList(\@nineth_only_background);
													$combi_result_hash{$combi}{$nineth_element}{background_gene_list} = \@nineth_only_background;

													my @tenth_only_background = (@first_only, @second_only, @third_only, @fourth_only, @fifth_only, @sixth_only, @seventh_only, @eighth_only, @nineth_only);
													@tenth_only_background = &nonRedundantList(\@tenth_only_background);
													$combi_result_hash{$combi}{$tenth_element}{background_gene_list} = \@tenth_only_background;
												} # if ($background eq 'other_gene_lists') {
											} # if (@intersection) {
										} # if ($combi_result_hash{$first_2nd_3rd_4th_5th_6th_7th_element}) {
										} # if (!$combi_result_hash{$combi}) {
									} # elsif ($combi_size == 10) {
								} # foreach my $combi (@combinations) {
			} # for (my $i=$size; $i>=2; $i--) {

### calculations are done, now print the results using %combi_result_hash and @all_combi
#print "srk : @all_combi<br>";
								my $z = 0;
								my $create_table_string = "";
								my $fh = "";
								my $gene_list_str = "";
								foreach my $combi (@all_combi) {
									if ($combi_result_hash{$combi}) {
										$z++;
										my $list_name_combi = $combi;
										my @combi = split(";", $combi);
                  	my $combi_size = scalar(@combi);	
										my @intersection = @{$combi_result_hash{$combi}{i}{gene_list}};
                    my $intersection_size = @intersection;
										my ($intersection_slashes, $how_many) = &getSlashes($biggest_gene_list_size, $intersection_size);
									print "<tr><td><br>";
										print "<table border=0 cellspacing=0 width=700>";
											my $first_element = shift @combi;
											my @first_only = @{$combi_result_hash{$combi}{$first_element}{gene_list}};
											my $first_only_size = @first_only;
											my $first_only_spaces = &getSpaces($biggest_gene_list_size, $first_only_size);
											$list_name_combi =~ s/;/_/g;	
											my $first_only_list_name = "gene_list__" . $list_name_combi . "__" . $first_element . "__L";
											my $intersect_list_name = "gene_list__" . $list_name_combi . "__I";
# creation of mysql tables & gene lists
											if(@intersection) {
												### creating intersection table
												$create_table_string = &create_table($intersect_list_name, \@intersection);
												print FH_MYSQL "$create_table_string";
	
												### creating intersection gene list file
												$fh = $session_dir . "$intersect_list_name";
										    close (FH);
										    open(FH,">$fh");
										    $gene_list_str = join("\n", @intersection);
										    print FH "$gene_list_str\n";
										    close (FH);
											} # if(@intersection) {
											if(@first_only) {
												### creating left first element list table
												$create_table_string = &create_table($first_only_list_name, \@first_only);
												print FH_MYSQL "$create_table_string";
	
												### creating left first element gene list file
												$fh = $session_dir . "$first_only_list_name";
										    close (FH);
										    open(FH,">$fh");
										    $gene_list_str = join("\n", @first_only);
										    print FH "$gene_list_str\n";
										    close (FH);
											} # if(@first_only) {
											if ($background eq 'other_gene_lists') {
												my @intersection_background_gene_list = @{$combi_result_hash{$combi}{i}{background_gene_list}};
												### creating intersection background file
												if (@intersection_background_gene_list) {
													$fh = $session_dir . "$intersect_list_name" . "__background";
									    		close (FH);
									    		open(FH,">$fh");
									    		$gene_list_str = join("\n", @intersection_background_gene_list);
									    		print FH "$gene_list_str\n";
									    		close (FH);
												} # if (@intersection_background_gene_list) {

												my @first_only_background_gene_list = @{$combi_result_hash{$combi}{$first_element}{background_gene_list}};
												### creating first only background file
												if (@first_only_background_gene_list) {
													$fh = $session_dir . "$first_only_list_name" . "__background";	
									    		close (FH);
									    		open(FH,">$fh");
									    		$gene_list_str = join("\n", @first_only_background_gene_list);
									    		print FH "$gene_list_str\n";
									    		close (FH);
												} # if (@first_only_background_gene_list) {
											} # if ($background eq 'other_gene_lists') {

											$first_element++;
#											print "<tr><td rowspan=$combi_size width='70'  class=biocompendium>$z</td><td width='70'  class=biocompendium>$first_element</td><td width='280'  class=biocompendium align=right>$first_only_size <a class=gene_list$first_element href=\"http://www.embl.de\">$first_only_spaces</a></td><td rowspan=$combi_size width='280'  class=biocompendium_intersect align=left><a class=intersect href=\"http://www.embl.de\">$intersection_slashes</a> $intersection_size</td></tr>";
											my $intersect_spaces = "&nbsp;" x (35 - $how_many);
											print "<tr><td rowspan=$combi_size width='70'  class=biocompendium>$z</td><td width='70'  class=biocompendium>$first_element</td><td width='280'  class=biocompendium align=right>$first_only_size <a class=gene_list$first_element lang=\"JavaScript\" onclick=\"overlib(list_option_text('$background', '$session', '$first_only_list_name', '$primary_org'),STICKY,CAPTION,'$first_only_list_name',CLOSECLICK,HAUTO,OFFSETY,0);\">$first_only_spaces</a></td><td rowspan=$combi_size  class=biocompendium_intersect align=left><a class=intersect lang=\"JavaScript\" onclick=\"overlib(list_option_text('$background', '$session', '$intersect_list_name', '$primary_org'),STICKY,CAPTION,'$intersect_list_name',CLOSECLICK,HAUTO,OFFSETY,0);\">$intersection_slashes $intersection_size</a></td><td rowspan=$combi_size class=biocompendium_intersect_white><a class=intersect_white href=\"\">$intersect_spaces</a></td></tr>";
											foreach my $c (@combi) {
												my $element = $c+1;
												my @element_only = @{$combi_result_hash{$combi}{$c}{gene_list}};
												my $element_only_size = scalar(@element_only);
												my $element_only_spaces = &getSpaces($biggest_gene_list_size, $element_only_size);
												my $element_only_list_name = "gene_list__" . $list_name_combi . "__" . $c . "__L";

# creation of mysql tables & gene lists
												if (@element_only) {
													### creating rest of left element list table
													$create_table_string = &create_table($element_only_list_name, \@element_only);
													print FH_MYSQL "$create_table_string";
	
													### creating rest of left element gene list file
													$fh = $session_dir . "$element_only_list_name";
											    close (FH);
											    open(FH,">$fh");
											    $gene_list_str = join("\n", @element_only);
											    print FH "$gene_list_str\n";
											    close (FH);
												} # if (@element_only) {

												if ($background eq 'other_gene_lists') {
													### creating rest of left element background file
													my @element_only_background_gene_list = @{$combi_result_hash{$combi}{$c}{background_gene_list}};
													if (@element_only_background_gene_list) {
														$fh = $session_dir . "$element_only_list_name" . "__background";
                        		close (FH);
                        		open(FH,">$fh");
                        		$gene_list_str = join("\n", @element_only_background_gene_list);
                        		print FH "$gene_list_str\n";
                        		close (FH);
													} # if (@element_only_background_gene_list) {		
                      	} # if ($background eq 'other_gene_lists') {				
								
												print "<tr><td  class=biocompendium>$element</td><td  class=biocompendium align=right>$element_only_size <a class=gene_list$element lang=\"JavaScript\" onclick=\"overlib(list_option_text('$background', '$session', '$element_only_list_name', '$primary_org'),STICKY,CAPTION,'$element_only_list_name',CLOSECLICK,HAUTO,OFFSETY,0);\">$element_only_spaces</a></td></tr>";
											} # foreach my $c (@combi) {
										print "</table>";
									print "</td></tr>";
									} # if ($combi_result_hash{$combi}) {
								} # foreach my $combi (@all_combi) { 
							print "</table>\n";
						print "<br></td>\n";
					print "</tr>\n";
				print "</tbody>";			
} # if ($size > 1) { 
	close(FH_MYSQL);
	`/usr/bin/mysql -u srk -psrk -h elephant < $mysql_file`;
} # sub process_genelists {

sub get_gene_list {
	my ($org, $file, $id_doc_type, $primary_org, $session_dir) = @_;

	my $file_name = "";
	if ($file=~m/^.*(\\|\/)(.*)/){ # strip the remote path and keep the file_name 
	       	$file_name = $2;
       	}
       	else {
	       	$file_name = $file;
       	}

	my $dir_local_file = $session_dir . $file_name;
#print "dir_local_file : $dir_local_file<br>";
	
	my @ensembl_genes = (); 
	if ($id_doc_type eq "pdf" || $id_doc_type eq "doc" || $id_doc_type eq "excel" || $id_doc_type eq "ppt" || $id_doc_type eq "html" || $id_doc_type eq "ascii") {
		close(LOCAL);
		open(LOCAL, ">$dir_local_file") or die $!;
		while(<$file>) {
			print LOCAL $_;
		}
		close(LOCAL);

		my $tax_id = $tax_mappings{$org};
		my %reflect_input_hash = ('input_file'=>$dir_local_file,
					  'input_type'=>$id_doc_type,
					  'output_type'=>"ascii",
					  'output_file_name'=>"",
					  'organism'=>$tax_id
			);		
#print "tax_id : $tax_id<br>";
		my $reflected_bioentities = &Reflect::get_reflected_bioentities(%reflect_input_hash);
		my @reflected_bioentities = @$reflected_bioentities;
#		my %reflected_bioentities = %$reflected_bioentities;
#		my $proteins = $reflected_bioentities->{proteins};
#		my %proteins = %$proteins;
#		my $chemicals = $reflected_bioentities->{chemicals};
#		my %chemicals = %$chemicals;

		my @reflected_proteins_list = ();
		foreach my $p (@reflected_bioentities) {
#		foreach my $p (sort {$proteins{$a} cmp $proteins{$b}} keys %proteins) {
#my $description = &stitchAPI::getDescription($p);      
#print "p : $p, name : $proteins{$p}\n";
#print "p : $p, name : $proteins{$p}, des : $description\n";
			if ($p =~ /$tax_id/) {
#print "p : $p<br>";
				$p =~ s/$tax_id\.//;
				push @reflected_proteins_list, $p;
 			} # if ($p =~ /$tax_id/) {
		} # foreach my $p (sort {$proteins{$a} cmp $proteins{$b}} keys %proteins) {
			@reflected_proteins_list = &nonRedundantList(\@reflected_proteins_list);	
#print "reflected_proteins_list : @reflected_proteins_list<br>";
			$id_doc_type = "ensembl_peptide_id";

			@ensembl_genes = &IdMapper::get_ensembl_genes($org, \@reflected_proteins_list, $id_doc_type, $primary_org);
#print "ensembl_genes : @ensembl_genes<br>";

	} # if ($id_doc_type eq "pdf" || $id_doc_type eq "doc" || $id_doc_type eq "excel" || $id_doc_type eq "ppt" || $id_doc_type eq "html" || $id_doc_type eq "ascii") {
	else {
		my @id_list = ();
		while(<$file>) {
			my $id = $_;
#			chomp($id);
			$id =~ s/\n|\r//g;
			push @id_list, $id;
		}
#print "id_list : @id_list<br>";
		if ($id_doc_type eq "ensembl_gene_id" ) {
			@ensembl_genes = @id_list;
		} # if ($id_doc_type eq "ensembl_gene_id" ) {
		else {
			@ensembl_genes = &IdMapper::get_ensembl_genes($org, \@id_list, $id_doc_type, $primary_org);
		} # else 
#print "ensembl_genes : @ensembl_genes<br>";
	}
	@ensembl_genes = &nonRedundantList(\@ensembl_genes);
	return @ensembl_genes;
} # sub get_gene_list {


sub table_view {
	my ($position, $session, $list_name, $org, $sort_by_field_name, $asc_or_desc) = @_;
	my $banner = &get_browse_banner("");
#print "session : $session<br>";
#print "org : $org<br>";
#print "list_name : $list_name<br>";
	my $result_hash = 0;
	if($org eq "human") {
		$result_hash = &DbHumanGeneName::GetTableViewInfo($sort_by_field_name, $asc_or_desc, $session, $list_name);
	}
	elsif($org eq "mouse") {
		$result_hash = &DbMouseGeneName::GetTableViewInfo($sort_by_field_name, $asc_or_desc, $session, $list_name);
	}
	elsif($org eq "yeast") {
		$result_hash = &DbYeastGeneName::GetTableViewInfo($sort_by_field_name, $asc_or_desc, $session, $list_name);
	}
	my %result_hash = %$result_hash;

	my @keys = keys %result_hash;
	@keys = sort {$a <=> $b} @keys;
	my $size = scalar(@keys);
	print "<table cellpadding=\"0\" border=\"0\"  width=$table_width align=\"left\">\n";
		print "<tbody>";
			print "<tr>\n";
				print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description: </b></font></td>\n";
				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><br><b>Information from various biological sources in a short tabular view</b></font><br><br></td>\n";
			print "</tr>\n";
			print "<tr>\n";
				print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><br><b>No of Genes</b></font></td>\n";
				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>$size</b></font><br></td>\n";
			print "</tr>\n";
			print "<tr>\n";
				print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Legend</b></font></td>\n";
				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><i>: The following table is sortable</i><br></font></td>\n";
			print "</tr>\n";
	my $numdisplay = 30;
	$position++;
	$position--;
	
	my @subSet = splice(@keys, $position, $numdisplay);
	my $call_sub_table_view = &sub_table_view(\@subSet, $session, $list_name, $org, \%result_hash);
	my $total = $size;
	my ($nextstring,$prevstring,$firststring,$laststring,$startno,$endno) = &BuildNextPrevLinksForKeywordSearchSort("true", $total, $numdisplay, $position, $section, $org, $session, $list_name, $sort_by_field_name, $asc_or_desc);
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
		
	
# srk srk srk
} # sub table_view

sub sub_table_view {
	my ($keys, $session, $list_name, $org, $result_hash) = @_;

	my @keys = @$keys;
	my %result_hash = %$result_hash;

			print "<tr>\n";
				print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b></b></font></td>\n";
				print "<td><br>";
						print "<table cellspacing='0'>\n";
		print "<tr>\n";
			print "<td>";
				print "<table border=0 cellspacing='1'>\n";

					my $asc_link_img = "desc.png";
					my $desc_link_img = "asc.png";
					my $gene_asc_desc = "<table><tr><td>Gene</td><td><table><tr><td><a href=\"$URL_cgi?section=biodb&pos=0&org=$org&session=$session&list=$list_name&sort=gene&ad=desc\"><img alt=\"\" src=\"/images/$desc_link_img\" width=$hyper_link_img_width height=$hyper_link_img_height border='0'></a></td></tr><tr><td><a href=\"$URL_cgi?section=biodb&pos=0&org=$org&session=$session&list=$list_name&sort=gene&ad=asc\"><img alt=\"\" src=\"/images/$asc_link_img\" width=$hyper_link_img_width height=$hyper_link_img_height border='0'></a></td></tr></table></td></tr></table>";
					my $name_asc_desc = "<table><tr><td>Name</td><td><table><tr><td><a href=\"$URL_cgi?section=biodb&pos=0&org=$org&session=$session&list=$list_name&sort=name&ad=desc\"><img alt=\"\" src=\"/images/$desc_link_img\" width=$hyper_link_img_width height=$hyper_link_img_height border='0'></a></td></tr><tr><td><a href=\"$URL_cgi?section=biodb&pos=0&org=$org&session=$session&list=$list_name&sort=name&ad=asc\"><img alt=\"\" src=\"/images/$asc_link_img\" width=$hyper_link_img_width height=$hyper_link_img_height border='0'></a></td></tr></table></td></tr></table>";
					my $description_asc_desc = "<table><tr><td>Description</td><td><table><tr><td><a href=\"$URL_cgi?section=biodb&pos=0&org=$org&session=$session&list=$list_name&sort=description&ad=desc\"><img alt=\"\" src=\"/images/$desc_link_img\" width=$hyper_link_img_width height=$hyper_link_img_height border='0'></a></td></tr><tr><td><a href=\"$URL_cgi?section=biodb&pos=0&org=$org&session=$session&list=$list_name&sort=description&ad=asc\"><img alt=\"\" src=\"/images/$asc_link_img\" width=$hyper_link_img_width height=$hyper_link_img_height border='0'></a></td></tr></table></td></tr></table>";


					 print "<tr>\n";
						print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>$name_asc_desc </b></font></td>\n";
						print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>$description_asc_desc </b></font></td>\n";		
						print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>$gene_asc_desc </b></font></td>\n";
					print "</tr><tbody>\n";
					my $i = 0;
					foreach my $k (@keys) {
						$i++;
						my $bg;
						if($i%2==0) {
							$bg="#D4EDF4";
						}
						else {
							$bg="#cfc3f3";
						}
						my $name = $result_hash{$k}{name};
						my $description = $result_hash{$k}{description};
						my $gene = $result_hash{$k}{gene};
						my $gene_url = "http://www.ensembl.org/$org_mappings{$org}/geneview?gene=$gene";

							print "<tr bgcolor=\"$bg\">\n";
								print "<td width=10%><font face=\"Arial\" size=\"2\" color=\"#000000\"><a href=\"$URL_cgi?section=summary_sheet&gene=$gene&org=$org\">$name</a></font></td>\n";
								print "<td width=75%><font face=\"Arial\" size=\"2\" color=\"#000000\">$description</font></td>";
								print "<td width=15%><font face=\"Arial\" size=\"2\" color=\"#000000\"><a class=biocompendium href=\"$gene_url\">$gene</font></td>";
							print "</tr>\n";
					} # foreach my $k (@keys) {
				print "</tbody></table>\n";
			print "</tr>\n";
	print "</table>\n";		
} # sub sub_table_view {


sub summary_sheet {
	my ($gene, $org) = @_;
use DbHumanSummarySheet;
use DbMouseSummarySheet;
use DbYeastSummarySheet;

use DbHumanOrthology;
use DbMouseOrthology;
use DbYeastOrthology;

use DbDrugbankCidSid;
	my $banner = &get_browse_banner("");
	my $summary_sheet = 0;
	my $geneDetails = 0;
	my $gene_name_obj = 0;
	if ($org eq 'human') {
		$summary_sheet = new DbHumanSummarySheet($gene);
		$geneDetails   = new DbHumanGeneProtein($gene);
		$gene_name_obj = new DbHumanGeneName($gene);
	}
	elsif ($org eq 'mouse') {
		$summary_sheet = new DbMouseSummarySheet($gene);
		$geneDetails   = new DbMouseGeneProtein($gene);
		$gene_name_obj = new DbMouseGeneName($gene);
	}
	elsif ($org eq 'yeast') {
		$summary_sheet = new DbYeastSummarySheet($gene);
		$geneDetails   = new DbYeastGeneProtein($gene);	
		$gene_name_obj = new DbYeastGeneName($gene);
	}
# from summary_sheet object
	my $id = $summary_sheet->{DBID};
	$gene = $summary_sheet->{Gene};
	my $transcript = $summary_sheet->{Transcript};
	my $protein = $summary_sheet->{Protein};
	my $description = $summary_sheet->{Description};
	my $chr_name = $summary_sheet->{ChromosomeName};
	my $gene_start = $summary_sheet->{GeneStart};
	my $gene_end = $summary_sheet->{GeneEnd};
	my $go = $summary_sheet->{GO};
	my $embl_genbank_id = $summary_sheet->{EmblGenbankID};
	my $entrezgene_id = $summary_sheet->{EntrezgeneID};
	my $unigene_id = $summary_sheet->{UnigeneID};
	my $interpro = $summary_sheet->{Interpro};
	my $protein_id = $summary_sheet->{ProteinID};
	my $pdb_id = $summary_sheet->{PdbID};
	my $pdb_from_pdb = $summary_sheet->{PdbFromPdb};
	my $pdb_from_pssh = $summary_sheet->{PdbFromPssh};
	my $hssp_id = $summary_sheet->{HsspID};
	my $pssh_id = $summary_sheet->{PsshID};
	my $prosite_id = $summary_sheet->{PrositeID};
	my $prints_id = $summary_sheet->{Printsid};
	my $refseq_dna_id = $summary_sheet->{RefseqDNAID};
	my $refseq_peptide_id = $summary_sheet->{RefseqPeptideID};
#	my $refseq_predicted_dna_id = $summary_sheet->{RefseqPredictedDNAID};
	my $pfam_id = $summary_sheet->{PfamID};
#	my $unified_uniprot_id = $summary_sheet->{UnifiedUniprotID};
#	my $unified_uniprot_acc = $summary_sheet->{UnifiedUniprotAccession};
	my $unified_uniprot = $summary_sheet->{UniprotID};
	my $omim = $summary_sheet->{Omim};
	my $panther = $summary_sheet->{Panther};
	my $pathway = $summary_sheet->{Pathway};
#	my $reactome = $summary_sheet->{Reactome};
	my $drugbank = $summary_sheet->{Drugbank};
#	my $drugbank_drug_target = $summary_sheet->{DrugbankDrugTarget};
#	my $drugbank_metabolizing_enzyme = $summary_sheet->{DrugbankMetabolizingEnzyme};
	my $hmdb = $summary_sheet->{Hmdb};
#	my $hmdb_metabolic_enzyme = $summary_sheet->{HmdbMetabolicEnzyme};
#	my $hmdb_macromolecular_interacting_partner = $summary_sheet->{HmdbMacromolecularInteractingPartne};
#	my $hugo_name = $summary_sheet->{HugoName};
#	my $progeria_id = $summary_sheet->{ProgeriaID};

# from geneDetails object
	my $longest_protein = $geneDetails->{LongestProtein};
	my $GenomeDBID = $geneDetails->{GID}; 
# from gene_name_obj
	my $gene_name = $gene_name_obj->{name};

	my @unified_uniprot1 = split("______", $unified_uniprot);
	my $uniprot = $unified_uniprot1[0];
	my ($uniprot_id, $uniprot_des_acc) = split("____", $uniprot);
	my ($uniprot_des, $uniprot_acc) = split("__", $uniprot_des_acc);
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

sub domain_clustering {
	my ($position, $session, $list, $org) = @_;
	my $banner = &get_browse_banner("");
use DbLink;
use IO::Socket::INET;
use SocketConf;

	my $session_dir = $outPutDir . "sessions/" . $session . "/";
	my $domain_sim_name = "$list" . "__domain_sim";
	my $domain_sim = $session_dir . $domain_sim_name;

	my @ensembl_proteins = &DbLink::GetProteinsForGeneList($session, $list, $org);

	my %socket_conf = &SocketConf::getSocketConf();

	my $ensembl_proteins_str = join("\n",@ensembl_proteins);	
	my $job_name = "domain";
	my $msg = $job_name."\n".$org."\n".$ensembl_proteins_str.$socket_conf{END_OF_MESSAGE_TAG}."\n";
#print "msg : $msg<br>";

	my $clint_socket = IO::Socket::INET->new( Proto => "tcp",
					   PeerAddr => $socket_conf{HOST},
					   PeerPort => $socket_conf{PORT}			
					 );	
	my $response = "";
	if ($ensembl_proteins_str) {
		$response = $clint_socket->send($msg);
	}
	$/ = "_END_OF_MESSAGE_";
	$response = <$clint_socket>;
	chomp($response);
	$/ = "\n";
#print "response : $response<br>";
	close($clint_socket);

	
	close(FH);
	open(FH, ">$domain_sim");
	print FH "$response\n";
	close(FH);

	my $domain_mcl_out = $domain_sim. "__mcl";
	my $mcl = $biocompendium_perl . "mcl.pl";
	system("perl $mcl $domain_sim > $domain_mcl_out");
	my $cluster = "";
	my $i = 0;
	my %MCLclusters = ();
	my %MCLclustersSize = ();
	if (-s $domain_mcl_out) {
		if(open(FH,"$domain_mcl_out")) {
			my @clusters= <FH>;
			close(FH);
			shift @clusters; # to get rif of first line i.e. "(clustering"
			pop @clusters; # to get rif of last line i.e. ")"
			while(@clusters){
				$i++;
				$cluster = shift @clusters;
				chop($cluster);
				my @mem = split(' ', $cluster);
				my $size = @mem;
				$MCLclustersSize{$i} = $size;
				push @{$MCLclusters{$i}}, @mem;
			}# while(@clusters){
		} # if(open(FH,"$domain_mcl_out")) {
	} # if (-s $domain_mcl_out) {
#print "session : $session<br>\n";
#print "list : $list<br>\n";
#print "org : $org<br>\n";
#print "domain_sim : $domain_sim<br>\n";
	my $numdisplay = 10;
	$position++;
	$position--;
	my @cluster_ids = sort { $MCLclustersSize{$b} <=> $MCLclustersSize{$a} } keys %MCLclustersSize;
	my $no_of_clusters = @cluster_ids;
	my @subSet = splice(@cluster_ids, $position, $numdisplay);
	my $total = &sub_domain_clustering(\@subSet, $no_of_clusters, $position, $org, \%MCLclusters);
	$total = $no_of_clusters;
	my ($nextstring,$prevstring,$firststring,$laststring,$startno,$endno) = &BuildNextPrevLinksForKeywordSearch("true", $total, $numdisplay, $position, $section, $org, $session, $list);
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

} # sub domain_clustering {


sub sub_domain_clustering {
use smart_descriptions;
	my ($cluster_ids, $no_of_clusters, $pos, $org, $MCLclusters) = @_;
	my @cluster_ids = @$cluster_ids;
	my %MCLclusters = %$MCLclusters;

	print "<table cellpadding=\"10\" border=\"0\"  width=$table_width>\n";
		print "<tbody>";
			my $imgNo = 0;
			print "<tr>\n";
				print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></font></td>\n";
				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Smart Domain Clustering Details</b></font><br></td>\n";
			print "</tr>\n";
			print "<tr>\n";
				print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>No. of  Clusters</b></font></td>\n";
				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>$no_of_clusters</b></font><br></td>\n";
			print "</tr>\n";
			print "<tr>\n";
				print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"></font></td>\n";
				print "<td><br><a href=\"#\" onclick=\"return toggleAll(\'expand\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'expand\' onClick=\'changeImage(\"expand\")\'></a> <font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Expand All</b></font><a href=\"#\" onclick=\"return toggleAll(\'collapse\')\"> <img alt=\"\" src=\"/images/minus.gif\" name=\'collapse\' onClick=\'changeImage(\"collapse\")\'></a> <font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Collapse All</b></font><br></td>\n";
			print "</tr>\n";
			print "<tr>\n";
				print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Clusters: </b></font></td>\n";
				print "<td><br>";
					print "<table cellspacing='2' border='0'>\n";

					my $i = 0;
					my $z = 0;
					foreach my $cluster_id (@cluster_ids) {
						$z++;
						my $cluster_display_id = $pos + $z;
							my @proteins = @{$MCLclusters{$cluster_id}};
							my $cluster_details = "";
							my $cluster_description = "";
							my $do_you_know_cluster_description = "No";
							my $cluster_structure = "";
							my $do_you_know_pdb_structure = "No";
							my $pdb_id = "";
							my @pdb_ids = ();
							my %pdb_hash = ();
							foreach my $protein (@proteins) {
								$i++;
								my $bg;
								if($i%2==0) {
									$bg="#D4EDF4";
								}
								else {
									$bg="#cfc3f3";
								}
								my $ensg = "";
								my $gene_protein_obj = "";
								my $gene_name_obj = "";
								my $domainInfo = "";
								if ($org eq 'human') {
									$ensg = &DbHumanGeneProtein::GetGeneForProtein($protein);
									$gene_protein_obj = new DbHumanGeneProtein($ensg);
									$gene_name_obj = new DbHumanGeneName($ensg);
									$domainInfo = &DbHumanSmartDomain::getSmartDomainInfoForProtein($protein);
								}
								elsif ($org eq 'mouse') {
									$ensg = &DbMouseGeneProtein::GetGeneForProtein($protein);	
									$gene_protein_obj = new DbMouseGeneProtein($ensg);
									$gene_name_obj = new DbMouseGeneName($ensg);
									$domainInfo = &DbMouseSmartDomain::getSmartDomainInfoForProtein($protein);
								}
								elsif ($org eq 'yeast') {
									$ensg = &DbYeastGeneProtein::GetGeneForProtein($protein);	
									$gene_protein_obj = new DbYeastGeneProtein($ensg);
									$gene_name_obj = new DbYeastGeneName($ensg);
									$domainInfo = &DbYeastSmartDomain::getSmartDomainInfoForProtein($protein);
								}
								my $description = $gene_protein_obj->{Description};
								my $GenomeDBID = $gene_protein_obj->{GID};
								my $name = $gene_name_obj->{name};

#								my $smart_domain_object = new DbProgeriaSmartDomain($protein);
#								my $protein_id = $smart_domain_object->{ProteinID};

#								my $summary_sheet_id = &DbProgeriaSummarySheet::GetIdForHugo($hugo_name);
#								my $summary_sheet = new DbProgeriaSummarySheet($summary_sheet_id);
#								my $pdb_from_pdb = $summary_sheet->{PdbFromPdb};
#								my $pdb_from_pssh = $summary_sheet->{PdbFromPssh};
#
#								if ($do_you_know_pdb_structure eq "No") {
#									if ($pdb_from_pdb) {
#										$pdb_id = lc($pdb_from_pdb);
#										push @pdb_ids, $pdb_id;
#										$do_you_know_pdb_structure = "Yes";
#										$pdb_hash{$pdb_id} = $hugo_name;
#									} # if ($pdb_from_pdb) {
#									else {
#										$pdb_id = lc($pdb_from_pssh);
#										push @pdb_ids, $pdb_id;
#										$pdb_hash{$pdb_id} = $hugo_name;
#									} # else {
#								} # if ($do_you_know_pdb_structure eq "No") { 
#
#								my $validation_str = &progeria_validation($hugo_name);
								my @domainInfo = @$domainInfo;

								my $domain_field = "";
								if (@domainInfo) {
									foreach my $d (@domainInfo) {
										my $description =  $d->{Description};
										my $start = $d->{Start};
										my $end = $d->{End};

										my $smart_des = &smart_descriptions::get_smart_description($description);
										if ($smart_des) {
											$smart_des =~ s/'|"//g;
											my ($smart_id, $definition, $detailed_description) = split /____/, $smart_des;
											my $smart_id_url = "<a class=biocompendium href=http://smart.embl.de/smart/do_annotation.pl?DOMAIN=$smart_id target=_blank>$smart_id</a>";
											my $domain_overlib = "<a class=biocompendium onmouseover=\"return overlib(\'<b>SMART ID:</b> $smart_id_url<br><b>Definition:</b> $definition<br><b>Description:</b> $detailed_description\',STICKY,CAPTION,'$description');\" onmouseout=\"nd();\">$description</a>";
											$description = $domain_overlib;	
										}	
										$domain_field .= $description . "[$start" . "-" . "$end]; ";
									} # foreach my $d (@domainInfo) {
								} # if (@domainInfo) {
								chop($domain_field);
								chop($domain_field);

								$cluster_details .= "<tr bgcolor=\"$bg\">\n";
								$cluster_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><a class=biocompendium href=\"http://www.ensembl.org/$ensembl_mappings{$GenomeDBID}/protview?peptide=$protein\">$name</font></td>\n";
								$cluster_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$description</font></td>\n";
								$cluster_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$domain_field</font></td>\n";
#								$cluster_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$validation_str</font></td>\n</tr>\n";
								if ($do_you_know_cluster_description eq "No") {
									$cluster_description = $description;
									if($description) {
										$do_you_know_cluster_description = "Yes";
									}
								}
							} # foreach my $protein (@proteins) {
							my $protein_str = join(" ", @proteins);

#							my $pdb_ids_size = @pdb_ids;
#							if ($pdb_ids_size > 1) {
#								$pdb_id = &get_most_repeated_element(\@pdb_ids);
#
#							}
#							else {
#								$pdb_id = $pdb_ids[0];
#							}
#							$cluster_structure = "pdb" . $pdb_id . ".ent " . $pdb_hash{$pdb_id};

						print "<tbody>";
							 print "<tr>\n";
								my $toggle = "cluster" . $cluster_id;
								$imgNo++;
								print "<td width=\"12%\" ><a href=\"#\" onclick=\"return toggleItem(\'$toggle\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> # Cluster: $cluster_display_id </b></font>";
								print "</td>\n";
								print "<td bgcolor= #dcdcdc><font face=\"Arial\" size=\"2\" color=\"#000000\">$cluster_description</font></td>\n";
								print "<td bgcolor= #dcdcdc><a href=\"$URL_cgi?section=graph_view&org=$org&proteins=$protein_str\"><font face=\"Arial\" size=\"2\" color=\"#000000\">Graph view</font></a></td>\n";
#								print "<td bgcolor= #dcdcdc>";
#									print "<applet code='jalview.bin.JalviewLite' width=\"140\" height=\"35\" archive='/biocompendium/temp/jalview/jalviewApplet.jar'>";
#										my $align_file = "";
#										print "<param name=\"file\" value=\"/biocompendium/temp/jalview/smart_clusters/cluster_${cluster_id}.afa\">";
#										print "<param name=\"defaultColour\" value=\"Clustal\">";
#										print "<param name=\"showFullId\" value=\"false\">";
#										print "<param name=\"PDBfile\"  value=\"/biocompendium/temp/jalview/pdb/$cluster_structure\">";
#									print "</applet>";
#								print "</td>";
							print "</tr>\n";
						print "</tbody>";
						print "<tbody class=\"collapse_obj\" id=\"$toggle\">\n";
							print "<tr>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Gene </b></font></td>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description </b></font></td>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Domains </b></font></td>\n";
#								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Group </b></font></td>\n";								
							print "</tr>\n";
							print "$cluster_details";
							print "<tr><td>&nbsp;</td><td></td><td></td></tr>";
						print "</tbody>\n";
					} # foreach my $cluster_id (@cluster_ids) {
				print "</table>\n";
			print "<br></td>";
		print "</tr>\n";
	print "</table>\n";
}# sub sub_smart_domain_clustering {

sub homology_clustering {
	my ($position, $session, $list, $org) = @_;
	my $banner = &get_browse_banner("");
use DbLink;
use IO::Socket::INET;
use SocketConf;

	my $session_dir = $outPutDir . "sessions/" . $session . "/";
	my $homology_sim_name = "$list" . "__homology_sim";
	my $homology_sim = $session_dir . $homology_sim_name;

	my @ensembl_proteins = &DbLink::GetProteinsForGeneList($session, $list, $org);

	my %socket_conf = &SocketConf::getSocketConf();

	my $ensembl_proteins_str = join("\n",@ensembl_proteins);	
	my $job_name = "homology";
	my $msg = $job_name."\n".$org."\n".$ensembl_proteins_str.$socket_conf{END_OF_MESSAGE_TAG}."\n";

	my $clint_socket = IO::Socket::INET->new( Proto => "tcp",
					   PeerAddr => $socket_conf{HOST},
					   PeerPort => $socket_conf{PORT}			
					 );	
	my $response = "";
	if ($ensembl_proteins_str) {
		$response = $clint_socket->send($msg);
	}
	$/ = "_END_OF_MESSAGE_";
	$response = <$clint_socket>;
	chomp($response);
	$/ = "\n";
	close($clint_socket);
	
	close(FH);
	open(FH, ">$homology_sim");
	print FH "$response\n";
	close(FH);

	my $homology_mcl_out = $homology_sim. "__mcl";
	my $mcl = $biocompendium_perl . "mcl.pl";
	system("perl $mcl $homology_sim > $homology_mcl_out");
	my $cluster = "";
	my $i = 0;
	my %MCLclusters = ();
	my %MCLclustersSize = ();
	if (-s $homology_mcl_out) {
		if(open(FH,"$homology_mcl_out")) {
			my @clusters= <FH>;
			close(FH);
			shift @clusters; # to get rif of first line i.e. "(clustering"
			pop @clusters; # to get rif of last line i.e. ")"
			while(@clusters){
				$i++;
				$cluster = shift @clusters;
				chop($cluster);
				my @mem = split(' ', $cluster);
				my $size = @mem;
				$MCLclustersSize{$i} = $size;
				push @{$MCLclusters{$i}}, @mem;
			}# while(@clusters){
		} # if(open(FH,"$homology_mcl_out")) {
	} # if (-s $homology_mcl_out) {
#print "session : $session<br>\n";
#print "list : $list<br>\n";
#print "org : $org<br>\n";
#print "homology_sim : $homology_sim<br>\n";
	my $numdisplay = 10;
	$position++;
	$position--;
	my @cluster_ids = sort { $MCLclustersSize{$b} <=> $MCLclustersSize{$a} } keys %MCLclustersSize;
	my $no_of_clusters = @cluster_ids;
	my @subSet = splice(@cluster_ids, $position, $numdisplay);
	my $total = &sub_homology_clustering(\@subSet, $no_of_clusters, $position, $org, \%MCLclusters);
	$total = $no_of_clusters;
	my ($nextstring,$prevstring,$firststring,$laststring,$startno,$endno) = &BuildNextPrevLinksForKeywordSearch("true", $total, $numdisplay, $position, $section, $org, $session, $list);
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
} # sub homology_clustering {

sub sub_homology_clustering {
	my ($cluster_ids, $no_of_clusters, $pos, $org, $MCLclusters) = @_;
	my @cluster_ids = @$cluster_ids;
	my %MCLclusters = %$MCLclusters;

	print "<table cellpadding=\"10\" border=\"0\"  width=1200>\n";
		print "<tbody>";
			my $imgNo = 0;
			print "<tr>\n";
				print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></font></td>\n";
				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Homology Clustering Details</b></font><br></td>\n";
			print "</tr>\n";
			print "<tr>\n";
				print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>No. of  Clusters</b></font></td>\n";
				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>$no_of_clusters</b></font><br></td>\n";
			print "</tr>\n";
			print "<tr>\n";
				print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"></font></td>\n";
				print "<td><br><a href=\"#\" onclick=\"return toggleAll(\'expand\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'expand\' onClick=\'changeImage(\"expand\")\'></a> <font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Expand All</b></font><a href=\"#\" onclick=\"return toggleAll(\'collapse\')\"> <img alt=\"\" src=\"/images/minus.gif\" name=\'collapse\' onClick=\'changeImage(\"collapse\")\'></a> <font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Collapse All</b></font><br></td>\n";
			print "</tr>\n";
			print "<tr>\n";
				print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Clusters: </b></font></td>\n";
				print "<td><br>";
					print "<table cellspacing='2' border='0'>\n";

					my $i = 0;
					my $z = 0;
					foreach my $cluster_id (@cluster_ids) {
						$z++;
						my $cluster_display_id = $pos + $z;
							my @proteins = @{$MCLclusters{$cluster_id}};
							my $cluster_details = "";
							my $cluster_description = "";
							my $do_you_know_cluster_description = "No";
							my $cluster_structure = "";
							my $do_you_know_pdb_structure = "No";
							my $pdb_id = "";
							my @pdb_ids = ();
							my %pdb_hash = ();
							foreach my $protein (@proteins) {
								$i++;
								my $bg;
								if($i%2==0) {
									$bg="#D4EDF4";
								}
								else {
									$bg="#cfc3f3";
								}
								my $ensg = "";
								my $gene_protein_obj = "";
								my $gene_name_obj = "";
								if ($org eq 'human') {
									$ensg = &DbHumanGeneProtein::GetGeneForProtein($protein);
									$gene_protein_obj = new DbHumanGeneProtein($ensg);
									$gene_name_obj = new DbHumanGeneName($ensg);
								}
								elsif ($org eq 'mouse') {
									$ensg = &DbMouseGeneProtein::GetGeneForProtein($protein);	
									$gene_protein_obj = new DbMouseGeneProtein($ensg);
									$gene_name_obj = new DbMouseGeneName($ensg);
								}
								elsif ($org eq 'yeast') {
									$ensg = &DbYeastGeneProtein::GetGeneForProtein($protein);	
									$gene_protein_obj = new DbYeastGeneProtein($ensg);
									$gene_name_obj = new DbYeastGeneName($ensg);
								}
								my $description = $gene_protein_obj->{Description};
								my $GenomeDBID = $gene_protein_obj->{GID};
								my $name = $gene_name_obj->{name};

#								my $summary_sheet_id = &DbProgeriaSummarySheet::GetIdForHugo($hugo_name);
#								my $summary_sheet = new DbProgeriaSummarySheet($summary_sheet_id);
#								my $pdb_from_pdb = $summary_sheet->{PdbFromPdb};
#								my $pdb_from_pssh = $summary_sheet->{PdbFromPssh};
#
#								if ($do_you_know_pdb_structure eq "No") {
#									if ($pdb_from_pdb) {
#										$pdb_id = lc($pdb_from_pdb);
#										push @pdb_ids, $pdb_id;
#										$do_you_know_pdb_structure = "Yes";
#										$pdb_hash{$pdb_id} = $hugo_name;
#									} # if ($pdb_from_pdb) {
#									else {
#										$pdb_id = lc($pdb_from_pssh);
#										push @pdb_ids, $pdb_id;
#										$pdb_hash{$pdb_id} = $hugo_name;
#									} # else {
#								} # if ($do_you_know_pdb_structure eq "No") { 
#
#								my $validation_str = &progeria_validation($hugo_name);

								$cluster_details .= "<tr bgcolor=\"$bg\">\n";
								$cluster_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><a class=biocompendium href=\"http://www.ensembl.org/$ensembl_mappings{$GenomeDBID}/protview?peptide=$protein\">$name</font></td>\n";
								$cluster_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$description</font></td>\n";
#								$cluster_details .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$validation_str</font></td>\n</tr>\n";
								if ($do_you_know_cluster_description eq "No") {
									$cluster_description = $description;
									if($description) {
										$do_you_know_cluster_description = "Yes";
									}
								}
							} # foreach my $protein (@proteins) {

#							my $pdb_ids_size = @pdb_ids;
#							if ($pdb_ids_size > 1) {
#								$pdb_id = &get_most_repeated_element(\@pdb_ids);
#
#							}
#							else {
#								$pdb_id = $pdb_ids[0];
#							}
#							$cluster_structure = "pdb" . $pdb_id . ".ent " . $pdb_hash{$pdb_id};

						print "<tbody>";
							 print "<tr>\n";
								my $toggle = "cluster" . $cluster_id;
								$imgNo++;
								print "<td width=\"12%\" ><a href=\"#\" onclick=\"return toggleItem(\'$toggle\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> # Cluster: $cluster_display_id </b></font>";
								print "</td>\n";
								print "<td bgcolor= #dcdcdc><font face=\"Arial\" size=\"2\" color=\"#000000\">$cluster_description</font></td>\n";
#								print "<td bgcolor= #dcdcdc>";
#									print "<applet code='jalview.bin.JalviewLite' width=\"140\" height=\"35\" archive='/biocompendium/temp/jalview/jalviewApplet.jar'>";
#										my $align_file = "";
#										print "<param name=\"file\" value=\"/biocompendium/temp/jalview/smart_clusters/cluster_${cluster_id}.afa\">";
#										print "<param name=\"defaultColour\" value=\"Clustal\">";
#										print "<param name=\"showFullId\" value=\"false\">";
#										print "<param name=\"PDBfile\"  value=\"/biocompendium/temp/jalview/pdb/$cluster_structure\">";
#									print "</applet>";
#								print "</td>";
							print "</tr>\n";
						print "</tbody>";
						print "<tbody class=\"collapse_obj\" id=\"$toggle\">\n";
							print "<tr>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Gene </b></font></td>\n";
								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description </b></font></td>\n";
#								print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Group </b></font></td>\n";								
							print "</tr>\n";
							print "$cluster_details";
							print "<tr><td>&nbsp;</td><td></td></tr>";
						print "</tbody>\n";
					} # foreach my $cluster_id (@cluster_ids) {
				print "</table>\n";
			print "<br></td>";
		print "</tr>\n";
	print "</table>\n";
}# sub sub_smart_homology_clustering {

sub orthology {
	my ($position, $session, $list, $org) = @_;
	my $banner = &get_browse_banner("");
use DbLink;
	my @orthology_ids = &DbLink::GetOrthologyIdsForGeneList($session, $list, $org);

	my $numdisplay = 30;
	$position++;
	$position--;
	my $no_of_ids = @orthology_ids;
	my @subSet = splice(@orthology_ids, $position, $numdisplay);
	my $total = &sub_orthology(\@subSet, $no_of_ids, $position, $org);
	$total = $no_of_ids;
	my ($nextstring,$prevstring,$firststring,$laststring,$startno,$endno) = &BuildNextPrevLinksForKeywordSearch("true", $total, $numdisplay, $position, $section, $org, $session, $list);
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
} # sub orthology {


sub sub_orthology {
	my ($orthoIds, $no_of_ids, $position, $org) = @_;	
	my @orthoIds = @$orthoIds;
	print "<table cellpadding=\"10\" border=\"0\"  width=1200>\n";
		print "<tbody>";
	my $imgNo = 0;
			print "<tr>\n";
				print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></font></td>\n";
				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Orthology information for given list of genes</b></font><br></td>\n";
			print "</tr>\n";
			print "<tr>\n";
				print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"></font></td>\n";
				print "<td><br><a href=\"#\" onclick=\"return toggleAll(\'expand\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'expand\' onClick=\'changeImage(\"expand\")\'></a> <font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Expand All</b></font><a href=\"#\" onclick=\"return toggleAll(\'collapse\')\"> <img alt=\"\" src=\"/images/minus.gif\" name=\'collapse\' onClick=\'changeImage(\"collapse\")\'></a> <font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Collapse All</b></font><br></td>\n";
			print "</tr>\n";
			print "<tr>\n";
				print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>*:Orthology types</b></font></td>\n";
				print "<td><p style=\"font-family:verdana;font-size:80%;color:blue\">";
					print "one2one orthology";
					print "<br>one2many orthology";
					print "<br>many2many orthology";
					print "<br>apparent one2one orthology";
					print "<br>";
					print "<br><I><a href=\"http://oct2007.archive.ensembl.org/info/data/compara/homology_method.html\" target=\"_blank\">More information on orthology types</a></I></p>\n";
				print "</td>\n";
			print "</tr>\n";


		print "<tr>\n";
			print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Orthology Relations: </b></font></td>\n";
			print "<td><br>";
				print "<table cellspacing='2' border='0'>\n";
				my $i = 0;

				my %orthology = ();
				my %urlMap = ();
				my %speciesMap = ();
				foreach my $oid (@orthoIds) {
					my $orthology = "";
					if ($org eq 'human') {
						$orthology = new DbHumanOrthology($oid);
					}
					elsif ($org eq 'mouse') {
						$orthology = new DbMouseOrthology($oid);
					}
					elsif ($org eq 'yeast') {
						$orthology = new DbYeastOrthology($oid);
					}
					my $GeneDBID_des = $orthology->{GeneDBID};
					my ($GeneDBID, $gene_des) = split("\\[des\\]", $GeneDBID_des);
					my ($dbid, $Gene) = split(":", $GeneDBID);
					my $GenomeDBID = $orthology->{GenomeDBID};
					my $Orthologs= $orthology->{Orthologs};
					my $OrthologsDetails= $orthology->{OrthologsDetails};
					my $gene_name_obj = "";
					if ($org eq 'human') {
						$gene_name_obj = new DbHumanGeneName($Gene);
					}
					elsif ($org eq 'mouse') {
						$gene_name_obj = new DbMouseGeneName($Gene);
					}
					elsif ($org eq 'yeast') {
						$gene_name_obj = new DbYeastGeneName($Gene);
					}
					my $name = $gene_name_obj->{name};

					my @Ortho = split("__", $Orthologs);
					my $OrthoSize = @Ortho;
					my $orthology_details_table = ""; 
						my @OrthologsDetails = split("____", $OrthologsDetails);
						shift @OrthologsDetails;	
						foreach my $od (@OrthologsDetails) {
							my ($GeneDBID_des, $orthology_type) = split("__", $od);
							my ($GeneDBID, $gene_des) = split("\\[des\\]", $GeneDBID_des);
							my ($des, $hgnc) = split("\\[hgnc\\]", $gene_des);
							my ($dbid, $Gene) = split(":", $GeneDBID);
							if (!$hgnc) {
								$hgnc = $Gene;
							} # if (!$hgnc) {
							if ($dbid =~ /^\d+$/) {
				       	$orthology_details_table .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><i>$ensembl_mappings{$dbid}</i></font></td>";
								$orthology_details_table .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$orthotype{$orthology_type}</font></td>";
								$orthology_details_table .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><a class=biocompendium href=\"http://www.ensembl.org/$ensembl_mappings{$dbid}/geneview?gene=$Gene\">$hgnc</a></font></td>";
								$orthology_details_table .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$des</font></td><tr>";
							} # if ($dbid =~ /^\d+$/) {
						} # foreach my $od (@OrthologsDetails) {
				if ($orthology_details_table) {		
					print "<tbody>";
						print "<tr>\n";
							my $toggle = "orthology" . $oid;
							$imgNo++;
							print "<td width=\"12%\" ><a href=\"#\" onclick=\"return toggleItem(\'$toggle\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>$name</b></font>";
							print "</td>\n";
							print "<td bgcolor= #dcdcdc colspan=4><font face=\"Arial\" size=\"2\" color=\"#000000\">$gene_des</font></td>\n";
						print "</tr>\n";
					print "</tbody>";
				       	print "<tbody class=\"collapse_obj\" id=\"$toggle\">\n";
						print "<tr>\n";
							print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Organism </b></font></td>\n";
							print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Orthology type* </b></font></td>\n";
							print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Orthologs </b></font></td>\n";
							print "<td bgcolor= #c7c7d0><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Orthologs Description</b></font></td>\n";
						print "</tr>\n";
						print "<tr>$orthology_details_table";
						print "<tr><td>&nbsp;</td><td></td><td></td><td></td></tr>";
					print "</tbody>\n";
				} # if ($orthology_details_table) {	
			       	} # foreach my $oid (@orthoIds) {
			print "</table>\n";
		print "<br></td>";
		print "</tr>\n";
	print "</table>\n";
} # sub sub_orthology {

sub pathway {
	my ($position, $session, $list, $org) = @_;
	my $banner = &get_browse_banner("");
use DbLink;
	my $list_size = &DbLink::GeneListSize($session, $list, $org);
	my $kegg_result = &DbLink::GetKegg($session, $list, $org);
	my %kegg_result = %$kegg_result;
	my $kegg_hash = $kegg_result{kegg_hash};
	my %kegg_hash = %$kegg_hash;

	my $kegg_detail_hash = $kegg_result{kegg_detail_hash}; 
	my %kegg_detail_hash = %$kegg_detail_hash;

	my %kegg_size_hash = ();
	my %kegg_pvalue_hash = ();
	foreach my $kegg_id (keys %kegg_hash) {
    my @ids = @{$kegg_hash{$kegg_id}};
		my $size = scalar(@ids);						
		$kegg_size_hash{$kegg_id} = $size;
		my $p = &get_p_value($org, $kegg_id, $list_size, $size);
#		my $p = &get_p_value_jk($org, $kegg_id, $list_size, $size);
#print "kegg_id : $kegg_id p : $p";
	if ($p) {
			$kegg_pvalue_hash{$kegg_id} = $p;
		}
	}# foreach my $kegg_id (keys %kegg_hash) {

	my $corrected_pvalue_hash = &fdr_correction(\%kegg_pvalue_hash);
	my %corrected_pvalue_hash = %$corrected_pvalue_hash;
	my @kegg_ids = keys %kegg_pvalue_hash;
  my $no_of_pathways = scalar @kegg_ids;

	print "<table cellpadding=\"10\" border=\"0\"  width=1200>\n";
		print "<tbody>";
		print "<tr>\n";
			print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></font><br></td>\n";
			print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>&nbsp;&nbsp;Information from KEGG pathways - Mapping of given input genes</b></font><br></td>\n";
		print "</tr>\n";
		print "<tr>\n";
			print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>No of pathways mapped</b></font><br></td>\n";
			print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>&nbsp;&nbsp;$no_of_pathways</b></font><br></td>\n";
		print "</tr>\n";
		print "<tr>\n";
			print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b></b></font></td>\n";
			print "<td><br>";
			print "<table cellspacing='0'>\n";
				print "<tr>\n";
					print "<td>";
						print "<table border=0 cellspacing='1'>\n";
							print "<tr>\n";
								print "<td>";
									print "<table border=0 cellspacing='1'>\n";
					 print "<tr>\n";
						print "<td bgcolor= #c7c7d0 width=\"15%\"><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>KEGG Pathway ID </b></font></td>\n";
						print "<td bgcolor= #c7c7d0 width=\"40%\"><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>KEGG Pathway Name</b></font></td>\n";
						print "<td bgcolor= #c7c7d0 width=\"10%\"><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Adjusted P-Value</b></font></td>\n";
						print "<td bgcolor= #c7c7d0 width=\"15%\"><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Gene Name</b></font></td>\n";
						print "<td bgcolor= #c7c7d0 width=\"10%\"><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>KEGG Gene</b></font></td>\n";
						print "<td bgcolor= #c7c7d0 width=\"10%\"><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Ensmebl Gene</b></font></td>\n";
					print "</tr>\n";
	my $i = 0;	
	my $pathway_description = "";
#	foreach my $kegg_id (sort {$kegg_size_hash{$b}<=>$kegg_size_hash{$a}} keys %kegg_size_hash) {
#	foreach my $kegg_id (sort {$kegg_pvalue_hash{$a}<=>$kegg_pvalue_hash{$b}} keys %kegg_pvalue_hash) {
	foreach my $kegg_id (sort {$corrected_pvalue_hash{$a}<=>$corrected_pvalue_hash{$b}} keys %corrected_pvalue_hash) {
#print "kegg_id : $kegg_id p : $kegg_pvalue_hash{$kegg_id}";
#print "(adj : $corrected_pvalue_hash{$kegg_id})<br>";
		my $pathway_description = "";
		my $ids = $kegg_hash{$kegg_id};
		my @ids = @$ids;
		$i++;
		my $bg;
		if($i%2==0) {
			$bg="#D4EDF4";
		}
		else {
			$bg="#cfc3f3";
		}
			
		my $size = @ids;
		my $rowspan = $size+1;

		my $name_gene_str = "";
		my $kegg_genes_str = "";
		foreach my $id (@ids) {
			$pathway_description = $kegg_detail_hash{$id}{pathway_description};
			my $kegg_gene = $kegg_detail_hash{$id}{kegg_gene};
			$kegg_genes_str .= $kegg_gene . "+";
			$name_gene_str .= "<tr bgcolor=\"$bg\">\n";
			$name_gene_str .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$kegg_detail_hash{$id}{name}</font></td>\n";
			$name_gene_str .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><a class=biocompendium href=\"http://www.genome.jp/dbget-bin/www_bget?hsa+$kegg_gene\">$kegg_gene</a></font></td>\n";
			my $gene = $kegg_detail_hash{$id}{gene};
			$name_gene_str .= "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><a class=biocompendium href=\"http://www.ensembl.org/$org_mappings{$org}/geneview?gene=$gene\">$gene</a></font></td>\n";
		 	$name_gene_str .= "</tr>";
		} # foreach my $id (@ids) {

		my $kegg_pathway_url = "http://www.genome.jp/dbget-bin/show_pathway?" . $kegg_id . "+" . $kegg_genes_str;
		print "<tr bgcolor=\"$bg\">\n";
			print "<td rowspan=$rowspan><font face=\"Arial\" size=\"2\" color=\"#000000\"><a href=\"$kegg_pathway_url\"><img alt=\"\" src=\"/images/$hyper_link_flag_img\" width=$hyper_link_img_width height=$hyper_link_img_height border='0'></a> $kegg_id</font></td>\n";
			print "<td rowspan=$rowspan><font face=\"Arial\" size=\"2\" color=\"#000000\">$pathway_description</font></td>\n";
		my $adj_pvalue = sprintf("%.4e", $corrected_pvalue_hash{$kegg_id});
			print "<td rowspan=$rowspan><font face=\"Arial\" size=\"2\" color=\"#000000\">$adj_pvalue</font></td></tr>";
		print "</tr>";
		print "$name_gene_str\n";
#		print "<td rowspan=$rowspan><font face=\"Arial\" size=\"2\" color=\"#000000\">$corrected_pvalue_hash{$kegg_id}</font></td></tr>";
#		print "<td rowspan=$rowspan><font face=\"Arial\" size=\"2\" color=\"#000000\">$adj_pvalue</font></td></tr>";

	}# foreach my $kegg_id (keys %kegg_hash) {
											print "</table>";
										print "</td>";
									print "</tr>\n";
								print "</table>";
							print "</td>";
						print "</tr>\n";
					print "</table>";
				print "</td>";
			print "</tr>\n";
		print "</tbody>";
	print "</table>";
} # sub pathway {

sub chemistry {
	my ($position, $session, $list, $org) = @_;
	my $banner = &get_browse_banner("");
	my $session_dir = $outPutDir . "sessions/" . $session . "/";
	my $gene_list = $session_dir . $list;
	my @ensembl_gene_ids = ();
	close(FH);
	if (open(FH,$gene_list)){
		@ensembl_gene_ids = <FH>;
		chomp(@ensembl_gene_ids);
	} # if (open(FH,$gene_list)){ 
	close(FH);

	my $no_of_genes = scalar(@ensembl_gene_ids);
  print "<table cellpadding=\"10\" border=\"0\"  width=1200>\n";
    print "<tbody>";
      print "<tr>\n";
        print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></font></td>\n";
        print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Chemistry information</b></font><br></td>\n";
      print "</tr>\n";
	my $numdisplay = 5;
	$position++;
	$position--;
	my @subSet = splice(@ensembl_gene_ids, $position, $numdisplay);
	my $call_sub_chemistry = &sub_chemistry(\@subSet, $no_of_genes, $position, $org);
	my $total = $no_of_genes;
	my ($nextstring,$prevstring,$firststring,$laststring,$startno,$endno) = &BuildNextPrevLinksForKeywordSearch("true", $total, $numdisplay, $position, $section, $org, $session, $list);
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
} # sub chemistry {

sub sub_chemistry {
	my ($ensembl_genes, $no_of_genes, $pos, $org) = @_;
	my @ensembl_genes = @$ensembl_genes;
	print "<tr>\n";
  	print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"></font></td>\n";
    print "<td><br><a href=\"#\" onclick=\"return toggleAll(\'expand\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'expand\' onClick=\'changeImage(\"expand\")\'></a> <font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Expand All</b></font><a href=\"#\" onclick=\"return toggleAll(\'collapse\')\"> <img alt=\"\" src=\"/images/minus.gif\" name=\'collapse\' onClick=\'changeImage(\"collapse\")\'></a> <font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Collapse All</b></font><br></td>\n";
	print "</tr>\n";
	print "<tr>\n";
		print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b></b></font></td>\n";
		print "<td><br>";
			print "<table cellspacing='2' border='0'>\n";
			my $imgNo = 0;
			my $i = 0;
			foreach my $ensembl_gene (@ensembl_genes) {
      	$i++;
      	my $bg;
      	if($i%2==0) {
      		$bg="#D4EDF4";
      	}
      	else {
      		$bg="#cfc3f3";
      	}
				print "<tbody>";
					print "<tr>\n";
					my $toggle = "ensembl_gene" . $ensembl_gene;
					$imgNo++;
					my $gene_protein_obj = "";
					my $gene_name_obj = "";
					if ($org eq 'human') {
						$gene_protein_obj = new DbHumanGeneProtein($ensembl_gene);
						$gene_name_obj = new DbHumanGeneName($ensembl_gene);
					}
					elsif ($org eq 'mouse') {
						$gene_protein_obj = new DbMouseGeneProtein($ensembl_gene);
						$gene_name_obj = new DbMouseGeneName($ensembl_gene);
					}
					elsif ($org eq 'yeast') {
						$gene_protein_obj = new DbYeastGeneProtein($ensembl_gene);
						$gene_name_obj = new DbYeastGeneName($ensembl_gene);
					}
					my $name = $gene_name_obj->{name};
					my $ensembl_des = $gene_protein_obj->{Description};
						print "<td width=\"12%\" ><a href=\"#\" onclick=\"return toggleItem(\'$toggle\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> # $name </b></font>";
						print "</td>\n";
						print "<td bgcolor= #dcdcdc><font face=\"Arial\" size=\"2\" color=\"#000000\">$ensembl_des</font></td>\n";
						print "<td bgcolor= #dcdcdc><font face=\"Arial\" size=\"2\" color=\"#000000\"><a class=biocompendium href=\"http://www.ensembl.org/$org_mappings{$org}/geneview?gene=$ensembl_gene\">$ensembl_gene</a></font></td>\n";
					print "</tr>\n";
				print "</tbody>";
				print "<tbody class=\"collapse_obj\" id=\"$toggle\">\n";
						print "<tr>\n";
							print "<td></td>\n";
							print "<td>\n";
								print "<table cellspacing='2' border='0'>\n";
#drugs ...
									print "<tbody>";
										print "<tr>\n";
											my $detail_toggle = "drugs" . $toggle;
											$imgNo++;
											print "<td width=\"40%\" ><a href=\"#\" onclick=\"return toggleItem(\'$detail_toggle\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Drugs</b></font>";
											print "</td>\n";
											print "<td></td>\n";
										print "</tr>\n";
									print "</tbody>";

									my $chemistry = &get_chemistry($ensembl_gene, $org);
									my %chemistry = %$chemistry;
									my $drugs = $chemistry{drugs};
									my %drugs = %$drugs;

									my $drug_relevance = $chemistry{drug_relevance};
									my %drug_relevance = %$drug_relevance;

									print "<tbody class=\"collapse_obj\" id=\"$detail_toggle\">\n";
										 foreach my $drug (sort { $drug_relevance{$b} <=> $drug_relevance{$a} } keys %drug_relevance) {
										 	my $cid = $drugs{$drug}{cid};
											if($cid) {
												my $str = $drugs{$drug}{str};
												my $cid_link = $drugs{$drug}{cid_link};
												print "<tr>\n";
													print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\">$str</font></td>";
													my $cid_image = &get_chemical_structure($cid);
													print "<td><a href=\"$cid_link\" target=\"_blank\"><img src=\"$cid_image\" border=0></a></td></tr>";
												print "</tr>\n";
											} # if($cid) 
										} # foreach my $drug (sort { $drug_relevance{$b} <=> $drug_relevance{$a} } keys %drug_relevance) {									print "</tbody>\n";
									print "</tbody>\n";	

# ligands (pdb_ligand)
									print "<tbody>";
										print "<tr>\n";
										$detail_toggle = "ligands" . $toggle;
										$imgNo++;
											print "<td width=\"40%\" ><a href=\"#\" onclick=\"return toggleItem(\'$detail_toggle\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Ligands</b></font>";
											print "</td>\n";
											print "<td></td>\n";
										print "</tr>\n";
									print "</tbody>";
									my $ligands = $chemistry{ligands};
									my %ligands = %$ligands;

									print "<tbody class=\"collapse_obj\" id=\"$detail_toggle\">\n";
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

#metabolities (hmdb)
										print "<tbody>";
											print "<tr>\n";
												$detail_toggle = "metabolites" . $toggle;
												$imgNo++;
												print "<td width=\"40%\" ><a href=\"#\" onclick=\"return toggleItem(\'$detail_toggle\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Metabolites</b></font>";
												print "</td>\n";
												print "<td></td>\n";
											print "</tr>\n";
										print "</tbody>";

										my $metabolites = $chemistry{metabolites};
										my %metabolites = %$metabolites;
										print "<tbody class=\"collapse_obj\" id=\"$detail_toggle\">\n";
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
											$detail_toggle = "other" . $toggle;
											$imgNo++;
												print "<td width=\"40%\" ><a href=\"#\" onclick=\"return toggleItem(\'$detail_toggle\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Others</b></font>";
												print "</td>\n";
												print "<td></td>\n";
											print "</tr>\n";
										print "</tbody>";

										my $other_chemicals = $chemistry{other_chemicals};
										my %other_chemicals = %$other_chemicals;
										my $other_chemical_relevance = $chemistry{other_chemical_relevance};
										my %other_chemical_relevance = %$other_chemical_relevance;
										print "<tbody class=\"collapse_obj\" id=\"$detail_toggle\">\n";
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
						print "</tbody>\n";
			} # foreach my $ensembl_gene (@ensembl_genes) {
} # sub sub_chemistry {

sub go {
	my ($background, $position, $session, $list, $org) = @_;
	my $banner = &get_browse_banner("");

	my @domains = ("biological_process","molecular_function","cellular_component");
	my $go_perl_script = $biocompendium_perl . "GO/go_wrapper.pl"; 
	my $session_dir = $outPutDir . "sessions/" . $session . "/";
	my $go_result_file = "";
	foreach my $domain (@domains) {
		$go_result_file = $session_dir . $list . "__" . $domain;
		unless (-e $go_result_file) {
			system("perl $go_perl_script $session $list $org $background $domain");
		}
	} # foreach my $domain (@domains) {

	print "<table cellpadding=\"10\" border=\"0\"  width=$table_width>\n";
		print "<tbody>";
		my $imgNo = 0;
		print "<tr>\n";
			print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></font><br></td>\n";
			print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>&nbsp;&nbsp;Gene Ontology (GO) Information</b></font><br></td>\n";
		print "</tr>\n";
	print "<tr>\n";
		print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"></font></td>\n";
		print "<td><a href=\"#\" onclick=\"return toggleAll(\'expand\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'expand\' onClick=\'changeImage(\"expand\")\'></a> <font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Expand All</b> </font><a href=\"#\" onclick=\"return toggleAll(\'collapse\')\"> <img alt=\"\" src=\"/images/minus.gif\" name=\'collapse\' onClick=\'changeImage(\"collapse\")\'></a> <font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Collapse All</b></font><br></td>\n";
	print "</tr>\n";
	my $molecular_function_imgNo = &molecular_function($imgNo, $session, $list );
	my $biological_process_imgNo = &biological_process($molecular_function_imgNo, $session, $list);
	my $cellular_component_imgNo = &cellular_component($biological_process_imgNo, $session, $list);
	print "</tbody>";
print "</table>";
} # sub go {

sub molecular_function {
	my ($imgNo, $session, $list) = @_;
	my $session_dir = $outPutDir . "sessions/" . $session . "/";
	my $go_result_file = $session_dir . $list . "__" . "molecular_function";

	my %go_id2pval_hash = ();
	my %go_id2des_hash = ();
	if (-s $go_result_file) {
		close(FH);
		if (open(FH,$go_result_file)){
			while(<FH>) {
				chomp;
				my ($des, $go_id, $pvalue, $adj_pvalue, $term_freq) = split /\t/, $_;
#print "des :$des (go_id : $go_id) adj_pvalue : $adj_pvalue<br>";
				$go_id2pval_hash{$go_id}=$adj_pvalue;
				$go_id2des_hash{$go_id} = $des;
			} # while(<>) {
		} # if (open(FH,$go_result_file)){
		close(FH);
	} # if (-s $go_result_file) {

	print "<tr>\n";
		print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Molecular function</b></font></td>\n";
		print "<td>";
			print "<table cellspacing='0' width=$table_width>\n";
				print "<tbody>";
					print "<tr>\n";
					$imgNo++;
						print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_mf\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> Molecular function: </b></font>";
						print "</td>\n";
					print "</tr>\n";
				print "</tbody>";

				print "<tbody class=\"collapse_obj\" id=\"collapse_mf\">";
					print "<tr>\n";
						print "<td>";
								print "<table border=1 cellspacing='0'>\n";
									print "<tr>\n";
										print "<td bgcolor= #c7c7d0 width=10%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Accession</b></font></td>\n";
										print "<td bgcolor= #c7c7d0 width=80%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Term</b></font></td>\n";
										print "<td bgcolor= #c7c7d0 width=10%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Adjusted P-Value </b></font></td>\n";
									print "</tr>\n";

# srk srk 007
								my $i = 0;
								foreach my $gid (sort {$go_id2pval_hash{$a}<=>$go_id2pval_hash{$b}} keys %go_id2pval_hash) {
									$i++;
 									my $bg;
									if($i%2==0) {
	  								$bg="#D4EDF4";
									}
									else {
	  								$bg="#cfc3f3";
									}
								print "<tr>\n";
									print "<td bgcolor=\"$bg\"><font face=\"Arial\" size=\"2\" color=\"#000000\">$gid</font></td>\n";
									print "<td bgcolor=\"$bg\"><font face=\"Arial\" size=\"2\" color=\"#000000\">$go_id2des_hash{$gid}</font></td>\n";
									print "<td bgcolor=\"$bg\"><font face=\"Arial\" size=\"2\" color=\"#000000\">$go_id2pval_hash{$gid}</font></td>\n";
								print "</tr>\n";
							} # foreach my $go_id (sort {$go_id2pval_hash{$a}<=>$go_id2pval_hash{$b}} keys %go_id2pval_hash) {
								print "</table>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";
				print "</table>\n";
			print "</td>\n";
		print "</tr>\n";
		return $imgNo;
} # sub molecular_function {

sub biological_process {
	my ($imgNo, $session, $list) = @_;
	my $session_dir = $outPutDir . "sessions/" . $session . "/";
	my $go_result_file = $session_dir . $list . "__" . "biological_process";

	my %go_id2pval_hash = ();
	my %go_id2des_hash = ();
	if (-s $go_result_file) {
		close(FH);
		if (open(FH,$go_result_file)){
			while(<FH>) {
				chomp;
				my ($des, $go_id, $pvalue, $adj_pvalue, $term_freq) = split /\t/, $_;
#print "des :$des (go_id : $go_id) adj_pvalue : $adj_pvalue<br>";
				$go_id2pval_hash{$go_id}=$adj_pvalue;
				$go_id2des_hash{$go_id} = $des;
			} # while(<>) {
		} # if (open(FH,$go_result_file)){
		close(FH);
	} # if (-s $go_result_file) {

	print "<tr>\n";
		print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Biological process</b></font></td>\n";
		print "<td>";
			print "<table cellspacing='0' width=$table_width>\n";
				print "<tbody>";
					print "<tr>\n";
					$imgNo++;
						print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_bp\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> Biological process : </b></font>";
						print "</td>\n";
					print "</tr>\n";
				print "</tbody>";

				print "<tbody class=\"collapse_obj\" id=\"collapse_bp\">";
					print "<tr>\n";
						print "<td>";
								print "<table border=1 cellspacing='0'>\n";
									print "<tr>\n";
										print "<td bgcolor= #c7c7d0 width=10%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Accession</b></font></td>\n";
										print "<td bgcolor= #c7c7d0 width=80%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Term</b></font></td>\n";
										print "<td bgcolor= #c7c7d0 width=10%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Adjusted P-Value </b></font></td>\n";
									print "</tr>\n";

# srk srk 007
								my $i = 0;
								foreach my $gid (sort {$go_id2pval_hash{$a}<=>$go_id2pval_hash{$b}} keys %go_id2pval_hash) {
									$i++;
 									my $bg;
									if($i%2==0) {
	  								$bg="#D4EDF4";
									}
									else {
	  								$bg="#cfc3f3";
									}
								print "<tr>\n";
									print "<td bgcolor=\"$bg\"><font face=\"Arial\" size=\"2\" color=\"#000000\">$gid</font></td>\n";
									print "<td bgcolor=\"$bg\"><font face=\"Arial\" size=\"2\" color=\"#000000\">$go_id2des_hash{$gid}</font></td>\n";
									print "<td bgcolor=\"$bg\"><font face=\"Arial\" size=\"2\" color=\"#000000\">$go_id2pval_hash{$gid}</font></td>\n";
								print "</tr>\n";
							} # foreach my $go_id (sort {$go_id2pval_hash{$a}<=>$go_id2pval_hash{$b}} keys %go_id2pval_hash) {
								print "</table>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";
				print "</table>\n";
			print "</td>\n";
		print "</tr>\n";
		return $imgNo;
} # sub biological_process {

sub cellular_component {
	my ($imgNo, $session, $list) = @_;
	my $session_dir = $outPutDir . "sessions/" . $session . "/";
	my $go_result_file = $session_dir . $list . "__" . "cellular_component";

	my %go_id2pval_hash = ();
	my %go_id2des_hash = ();
	if (-s $go_result_file) {
		close(FH);
		if (open(FH,$go_result_file)){
			while(<FH>) {
				chomp;
				my ($des, $go_id, $pvalue, $adj_pvalue, $term_freq) = split /\t/, $_;
#print "des :$des (go_id : $go_id) adj_pvalue : $adj_pvalue<br>";
				$go_id2pval_hash{$go_id}=$adj_pvalue;
				$go_id2des_hash{$go_id} = $des;
			} # while(<>) {
		} # if (open(FH,$go_result_file)){
		close(FH);
	} # if (-s $go_result_file) {

	print "<tr>\n";
		print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Cellular component</b></font></td>\n";
		print "<td>";
			print "<table cellspacing='0' width=$table_width>\n";
				print "<tbody>";
					print "<tr>\n";
					$imgNo++;
						print "<td><a href=\"#\" onclick=\"return toggleItem(\'collapse_cc\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> Cellular component: </b></font>";
						print "</td>\n";
					print "</tr>\n";
				print "</tbody>";

				print "<tbody class=\"collapse_obj\" id=\"collapse_cc\">";
					print "<tr>\n";
						print "<td>";
								print "<table border=1 cellspacing='0'>\n";
									print "<tr>\n";
										print "<td bgcolor= #c7c7d0 width=10%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Accession</b></font></td>\n";
										print "<td bgcolor= #c7c7d0 width=80%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Term</b></font></td>\n";
										print "<td bgcolor= #c7c7d0 width=10%><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Adjusted P-Value </b></font></td>\n";
									print "</tr>\n";

# srk srk 007
								my $i = 0;
								foreach my $gid (sort {$go_id2pval_hash{$a}<=>$go_id2pval_hash{$b}} keys %go_id2pval_hash) {
									$i++;
 									my $bg;
									if($i%2==0) {
	  								$bg="#D4EDF4";
									}
									else {
	  								$bg="#cfc3f3";
									}
								print "<tr>\n";
									print "<td bgcolor=\"$bg\"><font face=\"Arial\" size=\"2\" color=\"#000000\">$gid</font></td>\n";
									print "<td bgcolor=\"$bg\"><font face=\"Arial\" size=\"2\" color=\"#000000\">$go_id2des_hash{$gid}</font></td>\n";
									print "<td bgcolor=\"$bg\"><font face=\"Arial\" size=\"2\" color=\"#000000\">$go_id2pval_hash{$gid}</font></td>\n";
								print "</tr>\n";
							} # foreach my $go_id (sort {$go_id2pval_hash{$a}<=>$go_id2pval_hash{$b}} keys %go_id2pval_hash) {
								print "</table>";
							print "</td>\n";
						print "</tr>\n";
					print "</tbody>";
				print "</table>\n";
			print "</td>\n";
		print "</tr>\n";
		return $imgNo;
} # sub cellular_component {

sub transcription_factor {
	my ($position, $session, $list, $org) = @_;
	my $banner = &get_browse_banner("");
	my $human_header="BRCA1__Cebpa__CREB1__E2F1__ELK1__ELK4__ESR1__ETS1__FOXC1__FOXD1__FOXF2__FOXI1__FOXL1__GABPA__GATA2__GATA3__HLF__HNF4A__IRF1__IRF2__Lhx3__MAX__MEF2A__MIZF__MYC-MAX__Myf__MZF1_1-4__MZF1_5-13__NFIL3__NF-kappaB__NFKB1__NFYA__NHLH1__NKX3-1__NR1H2-RXRA__NR2F1__NR3C1__Pax6__PBX1__PPARG__PPARG-RXRA__REL__RELA__REST__RORA_1__RORA_2__RREB1__RXRA-VDR__SOX9__SP1__SPI1__SPIB__SRF__SRY__STAT1__TAL1-TCF3__TBP__TEAD1__TFAP2A__TLX1-NFIC__TP53__USF1__YY1__ZNF354C";
	my $mouse_header = "Arnt__Arnt-Ahr__T__Pax5__En1__Evi1__Gata1__Klf4__Nkx2-5__Pax2__Pax4__Prrx2__Sox17__Sox5__Hand1-Tcfe2a__Fos__Myb__Mycn__Spz1__Bapx1__Nobox__Pdx1__Lhx3__ELF5";
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
	if ($org ne 'yeast') {
		$tfbs_hash = &DbLink::GetTFBS($session, $list, $org);
	}
	else {
		print "No data generated for Yeast yet!!!";
	}
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
		system("/usr/local/bin/matrix2png -data $tfbs_matrix_file -r -c -s -size 15:15 -map 5  -range 0:100 > $tfbs_matrix2png_file");
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
use mouse_tfbs_matrix_map;
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


} # sub transcription_factor_details {

sub patent {
	my ($position, $session, $list, $org) = @_;
	my $banner = &get_browse_banner("");
  my $cut_off = 0.7;
use DbLink;
	my $patent_hash = &DbLink::GetPatent($session, $list, $org, $cut_off);
	my %patent_hash = %$patent_hash;

  my $numdisplay = 30;
	$position++;
	$position--;
	my @ensembl_genes = keys %patent_hash;
	my $no_of_genes = scalar(@ensembl_genes);
	my @subSet = splice(@ensembl_genes, $position, $numdisplay);
	my $total = &sub_patent(\@subSet, $no_of_genes, $position, $org, \%patent_hash, $cut_off);
	$total = $no_of_genes;
	my ($nextstring,$prevstring,$firststring,$laststring,$startno,$endno) = &BuildNextPrevLinksForKeywordSearch("true", $total, $numdisplay, $position, $section, $org, $session, $list);
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

} # sub patent {

sub sub_patent {
	my ($ensembl_genes, $no_of_clusters, $pos, $org, $primary_patent_hash, $cut_off) = @_;
	my @ensembl_genes = @$ensembl_genes;
	my %primary_patent_hash = %$primary_patent_hash;
	my %patent_offices = (
												"EPOP" => "European Patent Office", 
												"JPOP" => "Japan Patent Office", 
												"USPOP" => "United States Patent and Trademark Office", 
												"KPOP" => "Korean Patent Office" 
											);
	my %patent_dbs = (
												"EPOP" => "EPO_PRT", 
												"JPOP" => "JPO_PRT", 
												"USPOP" => "USPO_PRT", 
												"KPOP" => "KIPO_PRT" 
											);
use DbLink;
  print "<table cellpadding=\"10\" border=\"0\"  width=$table_width>\n";
    print "<tbody>";
      my $imgNo = 0;
    print "<tr>\n";
      print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></font><br></td>\n";
      print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>&nbsp;&nbsp;Patent information</b></font><br></td>\n";
    print "</tr>\n";

			print "<tr>\n";
				print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"></font></td>\n";
				print "<td><br><a href=\"#\" onclick=\"return toggleAll(\'expand\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'expand\' onClick=\'changeImage(\"expand\")\'></a> <font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Expand All</b></font><a href=\"#\" onclick=\"return toggleAll(\'collapse\')\"> <img alt=\"\" src=\"/images/minus.gif\" name=\'collapse\' onClick=\'changeImage(\"collapse\")\'></a> <font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Collapse All</b></font><br></td>\n";
			print "</tr>\n";
			print "<tr>\n";
				print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Patents: </b></font></td>\n";
				print "<td><br>";
					print "<table cellspacing='2' border='0'>\n";
					my $i = 0;
					foreach my $ensembl_gene (@ensembl_genes) {
						my $ensembl_protein = $primary_patent_hash{$ensembl_gene}{ens_protein};
						my $name = $primary_patent_hash{$ensembl_gene}{name};
						my $ensembl_des = $primary_patent_hash{$ensembl_gene}{des};
  					my $patent_result = &DbLink::GetPatentDetails($org, $ensembl_protein, $cut_off);
						my%patent_result = %$patent_result;
						my $patent_hash = $patent_result{patent_hash};
						my %patent_hash = %$patent_hash;
						my @patent_ids = sort { $patent_hash{$b} <=> $patent_hash{$a} } keys %patent_hash;
							
						my $patent_detail_hash = $patent_result{patent_detail_hash};
						my %patent_detail_hash = %$patent_detail_hash;
						
						print "<tbody>";
							 print "<tr>\n";
								my $toggle = "ensembl_gene" . $ensembl_gene;
								$imgNo++;
								print "<td width=\"12%\" ><a href=\"#\" onclick=\"return toggleItem(\'$toggle\')\"><img alt=\"\" src=\"/images/plus.gif\" name=\'img$imgNo\' onClick=\'changeImage(\"img$imgNo\")\'></a><font face=\"Arial\" size=\"2\" color=\"#000000\"><b> # $name </b></font>";
								print "</td>\n";
								print "<td bgcolor= #dcdcdc><font face=\"Arial\" size=\"2\" color=\"#000000\">$ensembl_des</font></td>\n";
								print "<td bgcolor= #dcdcdc><font face=\"Arial\" size=\"2\" color=\"#000000\"><a class=biocompendium href=\"http://www.ensembl.org/$org_mappings{$org}/geneview?gene=$ensembl_gene\">$ensembl_gene</a></font></td>\n";
							print "</tr>\n";
						print "</tbody>";
						print "<tbody class=\"collapse_obj\" id=\"$toggle\">\n";
							print "<tr><td></td><td>\n";
								print "<table>";
									my $z=0;
									foreach my $patent_id (@patent_ids) {
										$z++;
								    $i++;
								    my $bg;
    								if($i%2==0) {
      								$bg="#D4EDF4";
    								}
    								else {
      								$bg="#cfc3f3";
    								}
										my $patent_office = $patent_detail_hash{$patent_id}{patent_office};
										my $patent_id_url = "<a class=biocompendium href=\"http://srs.ebi.ac.uk/srsbin/cgi-bin/wgetz?-id+xx+-e+[$patent_dbs{$patent_office}:$patent_id]\">$patent_id</a>";
										my $nr_id = $patent_detail_hash{$patent_id}{nr_id};
										my $nr_id_url = "<a class=biocompendium href=\"http://srs.ebi.ac.uk/srsbin/cgi-bin/wgetz?-id+xx+-e+[NRPL2:$nr_id]\">$nr_id</a>";
										my $mf = $patent_detail_hash{$patent_id}{mf};
										my $mf_url = "<a class=biocompendium href=\"http://srs.ebi.ac.uk/srsbin/cgi-bin/wgetz?-id+xx+-e+[patentequivalents-ID:$mf]\">$mf</a>";
										my $des = $patent_detail_hash{$patent_id}{des};
										my $patent_from_de = $patent_detail_hash{$patent_id}{patent_from_de};
										my $patent_from_de_url = "";
										if ($patent_from_de =~ /([a-zA-Z]+)(\d+)/) {
											$patent_from_de_url = "<a class=biocompendium href=\"http://v3.espacenet.com/publicationDetails/biblio?CC=$1&NR=$2\">$patent_from_de</a>";
										}
										else {
											$patent_from_de_url = $patent_from_de;
										}
										my $mol_type = $patent_detail_hash{$patent_id}{mol_type};
										my $note = $patent_detail_hash{$patent_id}{note};
										$note =~ s/____/<br>/g; 
										print "<tr><td><table>";
											print"<tr><td class=biocompendium bgcolor=$bg><i><b>Patent Record #$z</b></i></td><td></td><tr>";
											print"<tr><td class=biocompendium bgcolor=$bg><b>Accession: </b></td><td class=biocompendium> $patent_id_url</td><tr>";
											print"<tr><td class=biocompendium bgcolor=$bg><b>Title: </b></td><td class=biocompendium> $patent_detail_hash{$patent_id}{title}</td><tr>";
											print"<tr><td class=biocompendium bgcolor=$bg><b>Significance: </b></td><td class=biocompendium> $patent_detail_hash{$patent_id}{frac_identical}</td></tr>";
											print"<tr><td class=biocompendium bgcolor=$bg><b>Patent office: </b></td><td class=biocompendium> $patent_offices{$patent_office}</td></tr>";
											print"<tr><td class=biocompendium bgcolor=$bg><b>Molecule type: </b></td><td class=biocompendium> $mol_type</td></tr>";
											print"<tr><td class=biocompendium bgcolor=$bg><b>Patent family: </b></td><td class=biocompendium> $mf_url</td></tr>";
											print"<tr><td class=biocompendium bgcolor=$bg><b>Non redundent patent ID: </b></td><td class=biocompendium> $nr_id_url</td></tr>";
											print"<tr><td class=biocompendium bgcolor=$bg><b>Publication number: </b></td><td class=biocompendium> $patent_from_de_url</td></tr>";
											print"<tr><td class=biocompendium bgcolor=$bg><b>Description: </b></td><td class=biocompendium> $des</td></tr>";
											print"<tr><td class=biocompendium bgcolor=$bg><b>Note: </b></td><td class=biocompendium> $note</td></tr>";
										print "</table></td></tr>";
									}# foreach my $patent_id (@patent_ids) {
								print "</table>";
							print "</td></tr>\n";
						print "</tbody>";
					} # foreach my $ensembl_gene (@ensembl_genes) {
					print "</table>\n";
				print "</td>";
		print "</tr>\n";
	print "</table>\n";
} # sub sub_patent {

sub clinical_trials {
	my ($position, $session, $list, $org) = @_;
	my $banner = &get_browse_banner("");
	print "<h1>Clinical trials section under development!!!</h1>";
} # sub clinical_trials {

## this sub routine provides protein - protein, protein-chemisty info from stitch ...
sub interaction {
	my ($position, $session, $list, $org) = @_;
	my $banner = &get_browse_banner("");

	my $session_dir = $outPutDir . "sessions/" . $session . "/";
	my $gene_list = $session_dir . $list;
	my @gene_list = ();
  close(FH);
  if (open(FH,$gene_list)){
		@gene_list = <FH>;
  	close(FH);
  } # if (open(FH,$gene_list)){

		my $gene_list_size = scalar @gene_list;
		my $gene_list_str = join("%0D", @gene_list);
		my $interactions_url = "";
		if ($gene_list_size > 1) {
			$interactions_url = "http://stitch.embl.de/interactionsList/$gene_list_str";
		}
		else {
			$interactions_url = "http://stitch.embl.de/interactions/$gene_list_str";	
		}
	
	print "<table cellpadding=\"10\" border=\"0\"  width=$table_width>\n";
		print "<tbody>";
		print "<tr>\n";
			print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><br><br><b>Protein-Protein, Protein-Chemistry interactions</b></font><br><br></td>\n";
			print "<td><br><br>&nbsp;&nbsp;<a href=\"$interactions_url\"><b>Protein-Protein, Protein-Chemical interaction network</a> for given list of proteins</b>\n";
			print "<br><br><br></td>\n";
		print "</tr>\n";
		print "</tbody>";
	print "</table>";
} # sub interaction {

# This method visualizes domain architecture of given list of ensembl proteins.... 
sub graph_view {
	my ($protein_str, $dbname, $org, $from) = @_;
	my @proteins = split(" ",$protein_str);
use DbHumanSmartDomain;
use DbMouseSmartDomain;
use DbYeastSmartDomain;
use smart_descriptions;
use Math::Round;
if ($from eq 'domain') {
	my $banner = &get_browse_banner("");
	print "<table cellpadding=\"10\" border=\"0\">\n";
		print "<tbody>";
			print "<tr>\n";
				print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></font></td>\n";
				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>$dbname domain cluster details</b></font><br></td>\n";
			print "</tr>\n";
			print "<tr>\n";
				print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</font></td>\n";
				print "<td><br>";
					print "<table cellspacing='0'>\n";
}
					print "<table cellspacing='0'>\n";
						 print "<tr>\n";
						 	print "<td><a href=\"http://smart.embl.de/\"><img src='/images/smart.png' width='10' height='10'></a> - Hyperlink to SMART; <a href=\"http://www.ensembl.org\"><img src='/images/e-bang.gif' width='10' height='10'></a> - Hyperlink to ENSEMBL</td>";
						print "</tr>\n";
						print "<tr>\n";
							print "<td>";
print "<table border=0 cellspacing='0'>\n";
	my $bg="#D4EDF4";
	print "<tr><td bgcolor=$bg></td><td bgcolor=$bg></td><td bgcolor=$bg></td><td bgcolor=$bg></td></tr>";
	print "<tr><td bgcolor=$bg></td><td bgcolor=$bg></td><td bgcolor=$bg></td><td bgcolor=$bg></td></tr>";
	print "<tr><td bgcolor=$bg></td><td bgcolor=$bg></td><td bgcolor=$bg></td><td bgcolor=$bg></td></tr>";
	print "<tr>\n";

	my @proteinIds = ();
	my @pp_mix_max = ();
	if ($org eq 'human') {
		@proteinIds = &DbHumanSmartDomain::GetProteinIdsForProteins(\@proteins);
		@pp_mix_max = &DbHumanSmartDomain::GetSmartProteinIdsDomainMaxMin(@proteinIds);
	}
	elsif ($org eq 'mouse') {
		@proteinIds = &DbMouseSmartDomain::GetProteinIdsForProteins(\@proteins);
		@pp_mix_max = &DbMouseSmartDomain::GetSmartProteinIdsDomainMaxMin(@proteinIds);
	}
	elsif ($org eq 'yeast') {
		@proteinIds = &DbYeastSmartDomain::GetProteinIdsForProteins(\@proteins);
		@pp_mix_max = &DbYeastSmartDomain::GetSmartProteinIdsDomainMaxMin(@proteinIds);
	}
	my $clusterSize = @proteinIds;
	my @min_max = ();
	if ($pp_mix_max[0]) {
		push @min_max, @pp_mix_max;
	}
	@min_max = sort {$a <=> $b} @min_max;
	my $min = $min_max[0];
	my $max = $min_max[-1];
	$max += 20; 
	my $factor = 1;
	if ($max > 500) {
		$factor = $max /500;
		$factor = round($factor);
	}

	my $height = 1;
	my $d_height = 31;
	my $vspace = 15;
	my @source = ("Pfam", "Prints", "Smart");
	my %s_url = ('Pfam' => '<a href=http://www.sanger.ac.uk/Software/Pfam>Pfam</a>',
		     'Prints' => '<a href=http://bioinf.man.ac.uk/dbbrowser/PRINTS>Prints</a>',
		     'Smart' => '<a href="http://smart.embl-heidelberg.de">Smart</a>'
		     );
	my %c = ('Pfam' => '/images/r1.png',
		 'Prints' => '/images/y.png',
		 'Smart' => '/images/g.png'
		);
	my $domainInfo;
	foreach my $c (@proteinIds) {
		my $protein = "";
		my $ensp = "";
		my $ensg = "";
		my $uniprot_id = "";
#		if ($dbname eq "Pfam") {
#			$protein = new DbGeneProtein($c);
#		}
#		else {
		my $longest_protein = "";
		my $protein_name = "";
		my $gene_name_obj = "";
		if ($org eq 'human') {
			$ensp = &DbHumanSmartDomain::GetProteinForProteinId($c);
			$ensg = &DbHumanGeneProtein::GetGeneForProtein($ensp);	
			$protein = new DbHumanGeneProtein($ensg);
			$gene_name_obj = new DbHumanGeneName($ensg);
		}
		elsif ($org eq 'mouse') {
			$ensp = &DbMouseSmartDomain::GetProteinForProteinId($c);
			$ensg = &DbMouseGeneProtein::GetGeneForProtein($ensp);	
			$protein = new DbMouseGeneProtein($ensg);
			$gene_name_obj = new DbMouseGeneName($ensg);
		}
		elsif ($org eq 'yeast') {
			$ensp = &DbYeastSmartDomain::GetProteinForProteinId($c);
			$ensg = &DbYeastGeneProtein::GetGeneForProtein($ensp);	
			$protein = new DbYeastGeneProtein($ensg);
			$gene_name_obj = new DbYeastGeneName($ensg);
		}
		$longest_protein = $protein->{LongestProtein};
		$protein_name = $gene_name_obj->{name};


		if ($dbname eq "Smart") {
			#$protein = "<a href=\"http://smart.embl.de/smart/show_motifs.pl?ID=$protein->{LongestProtein}\"><img src='/images/smart.png' width='10' height='10'></a>&nbsp;<a href=\"http://www.ensembl.org/$ensembl_mappings{$protein->{GID}}/protview?peptide=$protein->{LongestProtein}\"><img src='/images/e-bang.gif' width='10' height='10'></a>&nbsp;$protein->{LongestProtein}";
			$protein = "<a href=\"http://smart.embl.de/smart/show_motifs.pl?ID=$protein->{LongestProtein}\"><img src='/images/smart.png' width='10' height='10'></a>&nbsp;<a href=\"http://www.ensembl.org/$ensembl_mappings{$protein->{GID}}/protview?peptide=$protein->{LongestProtein}\"><img src='/images/e-bang.gif' width='10' height='10'></a>&nbsp;$protein_name";
		}	
#		elsif ($dbname eq "Pfam" && $uniprot_id) {
#			$protein = "<a href=\"http://www.sanger.ac.uk/cgi-bin/Pfam/swisspfamget.pl?name=$uniprot_id\"><img src='/images/pfam.gif' width='10' height='10'></a>&nbsp;<a href=\"http://www.ensembl.org/$ensembl_mappings{$protein->{GID}}/protview?peptide=$protein->{LongestProtein}\"><img src='/images/e-bang.gif' width='10' height='10'></a>&nbsp;$protein->{LongestProtein}";
#		}
		else {
			$protein = "<a href=\"http://www.ensembl.org/$ensembl_mappings{$protein->{GID}}/protview?peptide=$protein->{LongestProtein}\"><img src='/images/e-bang.gif' width='10' height='10'></a>&nbsp;$protein_name";
		}
	
		print "<td>&nbsp;&nbsp;&nbsp;</td><td>$protein</td>\n";
#		if ($dbname eq "Smart") {
		if ($org eq 'human') {
			$domainInfo = &DbHumanSmartDomain::getSmartDomainInfo($c);
		}
		elsif ($org eq 'mouse') {
			$domainInfo = &DbMouseSmartDomain::getSmartDomainInfo($c);
		}
		elsif ($org eq 'yeast') {
			$domainInfo = &DbYeastSmartDomain::getSmartDomainInfo($c);
		}

#		}
#		else {
#			$domainInfo = DomainArchitectureProgeria::getPfamDomainInfo($c);
#		}
		my @domainInfo = @$domainInfo;
		my @description = ();
		my @coordinates = ();
		my @tmp_x = ();
		my @tmp_y = ();
		if (@domainInfo) {
			foreach my $d (@domainInfo) {
my $d_des = $d->{Description};
#print "d : $d, d_des : $d_des\n";
				push @description, $d->{Description};
				push @tmp_x, $d->{Start};
				push @tmp_y, $d->{End};	
			} # foreach my $d (@domainInfo) {
		} # if (@domainInfo) {
		else {
			@tmp_x = 0;
			@tmp_y = 0;	
			@description = "NULL"; 
		} # else {
#print "description : @description\n";
		my $first = "";
		if ($tmp_x[0] == 0) {
			$first = "domain";
		} # if ($tmp_x[0] == 0) {	
		
		print "<td>&nbsp;&nbsp;&nbsp;</td><td>";
		my $start = 10 / $factor;
		my $overlap_flag = "NO";
		print "<table>";
		my $size_overlap_x;
my $n = 0;
		do {
#print "srk1 : $n  ";
			print "<tr><td>";
			if ($overlap_flag eq "NO") {
				print "<img src='/images/b.png' height='$height' width='$start' vspace='$vspace'>";
			}
			else {
				print "<img src='/images/e.png' height='$height' width='$start'>";
			}
			my $overlop = &getOverlap(\@tmp_x, \@tmp_y);
			my %overlop = %$overlop;
			my $x = $overlop{x};
			my @x = @$x;
#print "x : @x";
			my $y = $overlop{y};
			my @y = @$y;
			my $overlap_x = $overlop{overlap_x};
			my @overlap_x = @$overlap_x;
			my $overlap_y = $overlop{overlap_y};
			my @overlap_y = @$overlap_y;
			$size_overlap_x = @overlap_x;
			my $xsize = @x;
			my ($d_width, $width) = 0;
			my $last_y=0;
			for (my $i=0; $i<$xsize; $i++) {
############################################
				$d_width = 0;
				$width=0;
				my $domain_des = $description[$n];
				my $smart_des = &smart_descriptions::get_smart_description($domain_des);
				my $domain_overlib = "";
				if ($smart_des) {
					$smart_des =~ s/'|"//g;
					my ($smart_id, $definition, $detailed_description) = split /____/, $smart_des;
					my $smart_id_url = "<a class=biocompendium href=http://smart.embl.de/smart/do_annotation.pl?DOMAIN=$smart_id target=_blank>$smart_id</a>";
					$domain_overlib = "onmouseover=\"return overlib(\'<b>SMART ID:</b> $smart_id_url<br><b>Start:</b> $x[$i] <b> - Stop:</b> $y[$i]<br><b>Definition:</b> $definition<br><b>Description:</b> $detailed_description\',STICKY,CAPTION,'$domain_des');\" onmouseout=\"nd();\">";
				} else {
					$domain_overlib = "onmouseover=\"return overlib(\'<b>Start:</b> $x[$i] <b> - Stop:</b> $y[$i]\',STICKY,CAPTION,'$domain_des');\" onmouseout=\"nd();\">";
				}	
$n++;
				if ($dbname eq "Pfam") {
					$domain_des =~ s/:/_/;
				}
#print "xsize : $xsize, $i : $description[$n],  domain_des : $domain_des\n";
				my $domain_rep ="/images/SMART/Motifs/0.6/$domain_des.png";	      #"http://smart.embl.de/SMART_DATA/Motifs/0.6/$domain_des.png";
				if ($first eq "domain") {
#print "first";
					$d_width = $y[$i]-$x[$i];
					if ($i == ($xsize-1)) {
			 	       		$width = 0;
					}
					else {
						$width = $y[$i]-$x[$i+1];
					}
					$width = $width / $factor;
					$d_width = $d_width / $factor;
					
					if ($overlap_flag eq "NO") {
						print "<a class=biocompendium $domain_overlib<img src=\"$domain_rep\" height='$d_height' width='$d_width'></a><img src='/images/b.png' height='$height' width='$width'  vspace='$vspace'>";
					}
					else {
						print "<a class=biocompendium $domain_overlib<img src=\"$domain_rep\" height='$d_height' width='$d_width'></a><img src='/images/e.png' height='$height' width='$width'>";
					}
				}
			else {
#print "hello";
					if ($i == 0) {
						$width = $x[$i];
					}
					else {
						$width = $x[$i]-$y[$i-1];
					}
					$d_width = $y[$i]-$x[$i];
					$width = $width / $factor;
					$d_width = $d_width / $factor;
					if ($width > 0) {
						$last_y = $y[$i];
						if ($overlap_flag eq "NO") {
#print "overlap1";
							print "<img src='/images/b.png' height='$height' width='$width'  vspace='$vspace'><a class=biocompendium $domain_overlib<img src=\"$domain_rep\" height='$d_height' width='$d_width'></a>";	
						}
						else {
#print "overlap2";
							print "<img src='/images/e.png' height='$height' width='$width'><a class=biocompendium $domain_overlib<img src=\"$domain_rep\" height='$d_height' width='$d_width'></a>";
						}
					}
				}
			} # for (my $i=0; $i<@xsize; $i++) {
			$width = ($max - $last_y) / $factor;
			if ($overlap_flag eq "NO") {
#print "lala";
				print "<img src='/images/b.png' height='$height' width='$width'  vspace='$vspace'></td></tr>";
			}
			@tmp_x = @overlap_x;
			@tmp_y = @overlap_y;
			$overlap_flag = "YES";
		} while ($size_overlap_x != 0);
		print "</table>\n";
		print "</td></tr>\n";
	} # foreach my $c (@DetailsIds) {
	print "<tr></td><td bgcolor=$bg></td><td bgcolor=$bg></td><td bgcolor=$bg></td><td bgcolor=$bg></td></tr>";
	print "<tr></td><td bgcolor=$bg></td><td bgcolor=$bg></td><td bgcolor=$bg></td><td bgcolor=$bg></td></tr>";
	print "<tr></td><td bgcolor=$bg></td><td bgcolor=$bg></td><td bgcolor=$bg></td><td bgcolor=$bg></td></tr>";
	print "<tr><td><br></td><td></td><td></td><td></td></tr>";

									print "</tr>\n";
								print "</table>\n";
							print "</td>";
						print "</tr>\n";
					print "</table>\n";
				print "</td>";
			print "</tr>\n";
	if ($from eq 'domain') {
		print "</tbody>";
	print "</table>\n";
	}
} # sub graph_view {

sub getOverlap {
	my ($tmp_x, $tmp_y) =@_;
	my @tmp_x = @$tmp_x;
	my @tmp_y = @$tmp_y;
	my $size = @tmp_x;
	my (@x, @y, @overlap_x, @overlap_y)=();
	@x = $tmp_x[0];
	@y = $tmp_y[0];
	for (my $i=1; $i < $size; $i++) {
		if ($tmp_x[$i] < $y[-1]) {
			push @overlap_x, $tmp_x[$i];
			push @overlap_y, $tmp_y[$i];
		} # if ($tmp_x[$i] < $y[-1]) {
		else {
			push @x, $tmp_x[$i];
			push @y, $tmp_y[$i];
		} # else {
	} # for (my $i=1; $i < $size; $i++) {
	my %result = (x=>\@x, y=>\@y, overlap_x=>\@overlap_x, overlap_y=>\@overlap_y);
	\%result;
} # sub getOverlap {

sub get_chemistry {
	my ($gene, $org) = @_;
use DbHumanChemicals;
use DbHumanChemicalDetails;
use DbPubchemCidSid;
use DbDrugbankCidSid;
use DbHmdbCidSid;
use DbMatador;
use DbPdbLigand;
	my %drugs = ();
	my %drug_relevance = ();
	my %other_chemical_relevance = ();
	my %other_chemicals = ();
	my $summary_sheet = "";
	if ($org eq 'human') {
		my %chemicals_from_aks = &DbHumanChemicals::GetChemicalDetailsForGene($gene);
		foreach my $c (keys %chemicals_from_aks) {
       		       	my $relevance = $chemicals_from_aks{$c}{relevance};
			$relevance = sprintf("%.2f", $relevance);
       			my @bio_element_name = @{$chemicals_from_aks{$c}{bio_element_name}};
			my @cid = ();
			foreach my $ben (@bio_element_name) {
				if($ben =~ /cid/) {
					$ben =~ s/cid=//;
					push @cid, $ben;	
				}
				elsif($ben =~ /sid/) {
					$ben =~ s/sid=//;
					@cid = &DbPubchemCidSid::GetPubchemCidForSid($ben);
				}
			} # foreach my $ben (@bio_element_name) { 
			@cid = sort {$a <=> $b} @cid;
			my $cid = $cid[0];
			if($cid) {
				my $cid_link = $pubchem_url . $cid;
#print "cid : $cid\n";
				my $str = "<i>Name : </i>$c<br>";
				$str   .= "<i>Source : </i><a href=\"http://www.bioalma.com\">BioAlma</a><br>";
				$str   .= "<i>Relevance : </i>$relevance<br>";
				$str   .= "<i>PubChem cid : </i><a href=\"$cid_link\">$cid</a><br>";
	
				my $category = $chemicals_from_aks{$c}{category};
				if ($category){
					$drug_relevance{$c} = $relevance;

					$drugs{$c}{str} = $str;
					$drugs{$c}{cid_link} = $cid_link;
					$drugs{$c}{cid} = $cid;
		       		}
				else {
					$other_chemical_relevance{$c} = $relevance;
					$other_chemicals{$c}{str} = $str;
	    				$other_chemicals{$c}{cid_link} = $cid_link;
		    			$other_chemicals{$c}{cid} = $cid;
				}
			} # if($cid) {
       		} # foreach my $c (@chemicals_from_aks) {
		$summary_sheet = new DbHumanSummarySheet($gene);
	} # if ($org eq 'human') {
	elsif ($org eq 'mouse') {
		$summary_sheet = new DbMouseSummarySheet($gene);
	}
	elsif ($org eq 'yeast') {
		$summary_sheet = new DbYeastSummarySheet($gene);
	}


	
# add drugbank stuff to %drugs hash
	my $drugbank = $summary_sheet->{Drugbank};
	$drugbank =~ s/DRUGBANK:/$drugbank/g;
	my @drugbank = split("______", $drugbank);
	@drugbank = &nonRedundantList(\@drugbank);
	foreach my $d (@drugbank) {
       		my ($id, $des, $syn_pk) = split("____", $d);
		my ($syn, $pk) = split("__", $syn_pk);
		my $drugbank_obj = new DbDrugbankCidSid($pk);
	       	my $cid = $drugbank_obj->{cid};
		if ($des eq "" || $des eq "UNKNOWN") {
			$des = $drugbank_obj->{name};
		}
		my $cid_link = $pubchem_url . $cid;
		my $str = "<i>Name : </i>$des<br>";
		$str   .= "<i>Source : </i><a href=\"http://www.drugbank.ca/\">DrugBank</a><br>";
		$str   .= "<i>DrugBank id : </i><a href=\"http://www.drugbank.ca/drugs/$pk\">$pk</a><br>";
		$str   .= "<i>PubChem cid : </i><a href=\"$cid_link\">$cid</a><br>";
				
		$drug_relevance{$des} = 100;
		$drugs{$des}{str} = $str;
		$drugs{$des}{cid_link} = $cid_link;
		$drugs{$des}{cid} = $cid;
	} #foreach my $d (@drugbank) {				

# add matador stuff to %drugs hash
					
	my $protein = $summary_sheet->{Protein};
	my @protein = split(";", $protein);
	my @matador_cid_name = ();
	foreach my $p (@protein) {
		my $pk = "9606." . $p;
		my @cid_name = &DbMatador::GetPubchemCidNameForProtein($pk);
		push @matador_cid_name, @cid_name;
	} # foreach my $p (@protein) {	
	@matador_cid_name = &nonRedundantList(\@matador_cid_name);
					 
	foreach my $m (@matador_cid_name) {
		my ($cid, $name) = split("__", $m);
		my $cid_link = $pubchem_url . $cid;

		my $str = "<i>Name : </i>$name<br>";
		$str   .= "<i>Source : </i><a href=\"http://matador.embl.de\">Matador</a><br>";
		$str   .= "<i>Matador id : </i><a href=\"http://matador.embl.de/drugs/=$cid\">$cid</a><br>";
		$str   .= "<i>PubChem cid : </i><a href=\"$cid_link\">$cid</a><br>";

		$drug_relevance{$name} = 100;
		$drugs{$name}{str} = $str;
		$drugs{$name}{cid_link} = $cid_link;
		$drugs{$name}{cid} = $cid;
       } #foreach my $d (@drugbank) { 	

	my %ligands = ();
#ligands (pdb_ligand)
	my $pdb_id = $summary_sheet->{PdbID};
	my @pdb_id = split("______", $pdb_id);		
	my @pdb_pk = ();
	foreach my $p (@pdb_id) {
		my ($id, $des_pk) = split("____", $p);
		my ($des, $pk) = split("__", $des_pk);
		push @pdb_pk, lc($pk);
		my @pdb_ligand_ids = &DbPdbLigand::GetPdbLigandIdsForPdb($pk);
	} # foreach my $p (@pdb_id) {
	push @pdb_pk, lc($summary_sheet->{PdbFromPdb});
	push @pdb_pk, lc($summary_sheet->{PdbFromPssh});
	@pdb_pk = &nonRedundantList(\@pdb_pk);
											
	foreach my $pdb_pk (@pdb_pk) {
		my @pdb_ligand_ids = &DbPdbLigand::GetPdbLigandIdsForPdb($pdb_pk);
		foreach my $ligand (@pdb_ligand_ids){
			my $pdb_ligand_obj = new DbPdbLigand($ligand);
			my $cid = $pdb_ligand_obj->{pubchem_cid};
			if($cid) {
				my $cid_link = $pubchem_url . $cid;
				my $name = $pdb_ligand_obj->{name};
				my $str = "<i>Name : </i>$name<br>";
		  		$str   .= "<i>Source : </i><a href=\"http://www.rcsb.org\">PDB</a><br>";
				$str   .= "<i>PDB id : </i><a href=\"http://www.rcsb.org/pdb/explore/explore.do?structureId=$pdb_pk\">$pdb_pk</a><br>";
				$str   .= "<i>PubChem cid : </i><a href=\"$cid_link\">$cid</a><br>";

				$ligands{$name}{str} = $str;
				$ligands{$name}{cid_link} = $cid_link;
				$ligands{$name}{cid} = $cid;
			} # if($cid) {
		} # foreach my $ligand (@pdb_ligand_ids){
	} # foreach my $pdb_pk (@pdb_pk) {
										
#metabolites (hmdb)
	my %metabolites = ();
	my $hmdb = $summary_sheet->{Hmdb};
	my @hmdb = split("______", $hmdb);
       	@hmdb = &nonRedundantList(\@hmdb);
      	foreach my $h (@hmdb) {
       		my ($id, $des, $syn_pk) = split("____", $h);
		my ($syn, $pk) = split("__", $syn_pk);
		my $hmdb_obj = new DbHmdbCidSid($pk);
		my $cid = $hmdb_obj->{cid};
		if($cid) {
			my $cid_link = $pubchem_url . $cid;
			my $str = "<i>Name : </i>$des<br>";
			$str   .= "<i>Source : </i><a href=\"http://www.hmdb.ca\">HMDB</a><br>";
			$str   .= "<i>HMDB id : </i><a href=\"http://hmdb.ca/metabolites/$pk\">$pk</a><br>";
			$str   .= "<i>PubChem cid : </i><a href=\"$cid_link\">$cid</a><br>";

			$metabolites{$des}{str} = $str;
	       		$metabolites{$des}{cid_link} = $cid_link;
	       		$metabolites{$des}{cid} = $cid;
		}# if($cid) {		
	} #foreach my $h (@hmdb) {

	my %result = (drugs=>\%drugs, drug_relevance=>\%drug_relevance, ligands=>\%ligands, metabolites=>\%metabolites, other_chemicals=>\%other_chemicals, other_chemical_relevance=>\%other_chemical_relevance);
	return \%result;
} # sub get_chemistry {

sub get_chemical_structure {
	my $cid = shift;
	my $chunk = ($cid/25000);				       
	my $percent = $cid/25000;
	$percent = sprintf("%.d", $percent);	    
	my $mod = $cid%25000;
	if ($mod > 0) {
		$percent++;
	}		       
	my $start = ($percent - 1)*25000 + 1;		   
	my $end   = ($percent * 25000);
	my $chem_dir = "cid_" . $start . "_" . $end;
	my $cid_image = $chemistry_url . "/" . $chem_dir  . "/" .  $cid  .  ".png";
	return $cid_image;	      
} # sub get_chemical_structure { 


sub BuildNextPrevLinksForKeywordSearchSort {
    my ($blankon,$total,$numdisplay,$position, $section, $org, $session, $list_name, $sort_by_field_name, $asc_or_desc) = @_;
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

	my $prevlink = &EditQueryStringForKeywordSearchSort($prevstart, $section, $org, $session, $list_name, $sort_by_field_name, $asc_or_desc);
	$prevstring="<a href=\"$prevlink\">\< Previous </a>";

	my $firstlink = &EditQueryStringForKeywordSearchSort(0, $section, $org, $session, $list_name, $sort_by_field_name, $asc_or_desc);
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
	my $nextlink = &EditQueryStringForKeywordSearchSort($nextstart, $section, $org, $session, $list_name, $sort_by_field_name, $asc_or_desc);
	$nextstring="<a href=\"$nextlink\">Next \> ";

	my $lastpagenum = ($total % $numdisplay);
	my $laststart = $total - $lastpagenum;

	my $lastlink = &EditQueryStringForKeywordSearchSort($laststart, $section, $org, $session, $list_name, $sort_by_field_name, $asc_or_desc);
	$laststring="<a href=\"$lastlink\">Last \>\> </a>";
    }
    else {
	$nextstring="Next \>" if ($blankon);
	$laststring="Last \>\>" if ($blankon);
    }

    return ($nextstring,$prevstring,$firststring,$laststring,$startno,$endno);
} # sub BuildNextPrevLinksForKeywordSearchSort {

sub EditQueryStringForKeywordSearchSort {
	my ($pos, $section, $org, $session, $list_name, $sort_by_field_name, $asc_or_desc) = @_;
	my $link = "$URL_cgi?section=$section&pos=$pos&org=$org&session=$session&list=$list_name&sort=$sort_by_field_name&ad=$asc_or_desc";
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
sub get_banner {
		print "<!--      Developed by Venkata P. Satagopam   -->\n";
		print "<!--	     as part of his PhD thesis		   		 -->\n";
		print "<!--									   											 -->\n";
		print "<!--		venkata.satagopam\@embl.de	       		 -->\n";
		print "<!--									   											 -->\n";
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
} # sub get_banner {

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
} # sub get_browse_banner {

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

sub getSpaces {
	my ($biggest_gene_list_size, $gene_list_size) = @_;
	my $spaces = "";
	if ($gene_list_size > 0) {
		my $how_many = ($gene_list_size * 100)/$biggest_gene_list_size;
		$how_many = sprintf("%.d", $how_many);
		$spaces = "&nbsp;" x $how_many;
	}
	return $spaces;
} # sub getSpaces {
sub getSlashes {
	my ($biggest_gene_list_size, $gene_list_size) = @_;
	my $slashes = "";
	my $how_many = 0;
	if ($gene_list_size > 0) {
		$how_many = ($gene_list_size * 35)/$biggest_gene_list_size;
		$how_many = sprintf("%.d", $how_many);
		$slashes = "/" x $how_many;
	}
	return ($slashes, $how_many);
} # sub getSlashes {

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

sub get_p_value_jk {
	my ($org, $pathway_id, $list_size, $hit_size) = @_;
use Algorithms::Statistics;
use human_kegg_count;
use mouse_kegg_count;
use yeast_kegg_count;
	my $pathway_size = 0;
	my $all_genes_size = 0;
	if ($org eq 'human') {
	  $pathway_size = &human_kegg_count::get_kegg_count($pathway_id);
	  $all_genes_size = 36582;
	}
	if ($org eq 'mouse') {
	  $pathway_size = &mouse_kegg_count::get_kegg_count($pathway_id);
	  $all_genes_size = 28329;
	}
	if ($org eq 'yeast') {
	  $pathway_size = &yeast_kegg_count::get_kegg_count($pathway_id);
	  $all_genes_size = 7124;
	}

	my $a = $hit_size;
	my $b = $list_size - $hit_size;
	my $c = $pathway_size - $hit_size;
	my $d = $all_genes_size - ($a + $b + $c );

	my $contingency_table = [[$a,$b],[$c,$d]];
	my $p = Fishertest($contingency_table);
	return $p;
} # sub get_p_value_jk {

sub get_p_value {
	my ($org, $pathway_id, $list_size, $hit_size) = @_;
use Text::NSP::Measures::2D::Fisher::twotailed;
use human_kegg_count;
use mouse_kegg_count;
use yeast_kegg_count;
	my $pathway_size = 0;
	my $all_genes_size = 0;
	if ($org eq 'human') {
	  $pathway_size = &human_kegg_count::get_kegg_count($pathway_id);
	  $all_genes_size = 36582;
	}
	if ($org eq 'mouse') {
	  $pathway_size = &mouse_kegg_count::get_kegg_count($pathway_id);
	  $all_genes_size = 28329;
	}
	if ($org eq 'yeast') {
	  $pathway_size = &yeast_kegg_count::get_kegg_count($pathway_id);
	  $all_genes_size = 7124;
	}

	my $n11 = $hit_size;
	my $n1p = $list_size; 
	my $np1 = $pathway_size;
	my $npp = $all_genes_size;
#print "hit_size : $hit_size  (list_size : $list_size) pathway_size : $pathway_size (all_genes_size : $all_genes_size)";
	my $p = calculateStatistic( n11=>$n11,
			      n1p=>$n1p,
			      np1=>$np1,
			      npp=>$npp);
	return $p;
} # sub get_p_value {

sub fdr_correction {
  # False discovery rate by Benjamini and Hochberg method, taken from R (multtest library)
  # Adapted from perl code by Alvaro Mateos Gil

  my $kegg_pvalue_hash = shift;
	my %kegg_pvalue_hash = %$kegg_pvalue_hash;
  # Sort ids by p-value
  my @ids = sort {$kegg_pvalue_hash{$a}<=>$kegg_pvalue_hash{$b}} keys %kegg_pvalue_hash;

  my @spval;
  foreach my $id(@ids) {
    push @spval,$kegg_pvalue_hash{$id};
  }

  my $length_rawp = scalar @spval;

  my @adjp = @spval;
  my $j_index;
  for (my $j = $length_rawp-1; $j>=1; $j--) {
    $j_index = $j-1;
    $adjp[$j_index] = min($adjp[$j_index + 1], min(($length_rawp/$j) * $spval[$j_index], 1));
  }

  if (scalar @ids != scalar @spval || scalar @ids != scalar @adjp) {
    die "ERROR: sizes of output arrays differ\n";
  }

	my %corrected_pvalue_hash = ();
  foreach my $i(0..$#ids) {
#    $terms[$i]->{'corrected_p-value'} = $adjp[$i];
		$corrected_pvalue_hash{$ids[$i]} = $adjp[$i];
  }

  return \%corrected_pvalue_hash;
} # sub fdr_correction {

sub min {
  my ($a, $b) = @_;
  return $a<$b? $a : $b;
}
