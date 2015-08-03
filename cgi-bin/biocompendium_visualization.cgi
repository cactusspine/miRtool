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
my $section = $q->param( "section" );
my $position = $q->param("pos");
my $session = $q->param("session");
my $list = $q->param("list");
my $org = $q->param("org");
my $visualization_step1 = $q->param("visualization_step1");
my $visualization_step2 = $q->param("visualization_step2");
my @viz_genes = $q->param("viz_gene");
my @viz_domains = $q->param("viz_domain");
my $viz_tool = $q->param("viz_tool");
my $viz_genes_str = $q->param("viz_genes_str");

	if(!$section) {
		$section = "";
	}
	if(!$position) {
		$position = "";
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
	if(!$visualization_step1) {
		$visualization_step1 = "";
		@viz_genes = ();
	}
	if(!$visualization_step2) {
		$visualization_step2 = "";
		@viz_domains = ();
		$viz_tool = "";
		$viz_genes_str = "";
	}

my $host_name = "https://biocompendium.embl.de";
#my $URL_project = $host_name . "/biocompendium/";
my $URL_project = $host_name . "/";
my $URL_cgi = $host_name . "/cgi-bin/biocompendium.cgi";
my $STITCH_URL = "http://stitch.embl.de";
my $chemistry_url = $URL_project . "/temp/structure/";
my $pubchem_url = "http://pubchem.ncbi.nlm.nih.gov/summary/summary.cgi?cid=";
my $dasty2das_client = "http://www.ebi.ac.uk/dasty/client/ebi.php";
my $outPutDir = "/var/www/html/biocompendium/temp/";
my $cgi_dir = "/var/www/cgi-bin/";
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
	my $form_name = "biocompendium_visualization";
	my $method = "POST";
	my $action = "/cgi-bin/biocompendium_visualization.cgi";
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
	if ($section eq "visualization") {
		 &visualization($position, $session, $list, $org);
	}
	
	if ($visualization_step1 eq "Next") {
		&visualization_step1($session, $list, $org, \@viz_genes);
	}
	if ($visualization_step2 eq "Next") {
		&visualization_step2($session, $list, $org, $viz_genes_str, \@viz_domains, $viz_tool);
	}

	
print $q->endform;
print $q->end_html;


sub visualization {
	my ($position, $session, $list, $org) = @_;
	my $banner = &get_browse_banner("");
	my $sort_by_field_name = "name";
	my $asc_or_desc = "desc";
	my $result_hash = 0;
	if($org eq "human") {
		$result_hash = &DbHumanGeneName::GetTableViewInfo($sort_by_field_name, $asc_or_desc, $session, $list);
	}
	elsif($org eq "mouse") {
		$result_hash = &DbMouseGeneName::GetTableViewInfo($sort_by_field_name, $asc_or_desc, $session, $list);
	}
	elsif($org eq "yeast") {
		$result_hash = &DbYeastGeneName::GetTableViewInfo($sort_by_field_name, $asc_or_desc, $session, $list);
	}
	my %result_hash = %$result_hash;

	my @keys = keys %result_hash;
	@keys = sort {$a <=> $b} @keys;
	my $size = scalar(@keys);
	print "<table cellpadding=\"0\" border=\"0\"  width=$table_width align=\"left\">\n";
		print "<tbody>";
			print "<tr>\n";
				print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Step&nbsp;1:</b></font></td>\n";
				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><br><b>Select the genes to be visualized</b></font><br><br></td>\n";
			print "</tr>\n";
			print "<tr>\n";
				print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Gene selection</b></font></td>\n";
				print "<td><br>";
					print "<table cellspacing='0'>\n";

						print "<tr>\n";
							print "<td align=right><input type='submit' name='visualization_step1' value='Next'/><input type='hidden' name='org' value=\"$org\" />";
							print "</td>";
						print "</tr>\n";	

						print "<tr>\n";
							print "<td>";
								print "<table border=0 cellspacing='1'>\n";
					 print "<tr>\n";
						print "<td class=biocompendium_header><b>Select <input type=\"button\" name=\"CheckAll\" value=\"All\" onClick=\"checkAll(document.biocompendium_visualization.viz_gene)\"><input type=\"button\" name=\"UnCheckAll\" value=\"None\" onClick=\"uncheckAll(document.biocompendium_visualization.viz_gene)\"></b></td>\n";
						print "<td class=biocompendium_header><b>Name</b></td>\n";
						print "<td class=biocompendium_header><b>Description</b></td>\n";		
						print "<td class=biocompendium_header><b>Gene</b></td>\n";
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
						my $d = $description;
						$d =~ s/ /_/g;
						my $checkbox_value = $gene . "____" . $name . "____" . $d; 
						my $gene_url = "http://www.ensembl.org/$org_mappings{$org}/geneview?gene=$gene";
							print "<tr bgcolor=\"$bg\">\n";
								print "<td width=5% align=center><font face=\"Arial\" size=\"2\" color=\"#000000\"><INPUT TYPE=\"checkbox\" NAME=\"viz_gene\" VALUE=\"$checkbox_value\"></font></td>\n";
								print "<td width=10%><font face=\"Arial\" size=\"2\" color=\"#000000\">$name</font></td>\n";
								print "<td width=70%><font face=\"Arial\" size=\"2\" color=\"#000000\">$description</font></td>";
								print "<td width=15%><font face=\"Arial\" size=\"2\" color=\"#000000\"><a class=biocompendium href=\"$gene_url\">$gene</font></td>";
							print "</tr>\n";
					} # foreach my $k (@keys) {
				print "</tbody></table>\n";
			print "</tr>\n";

			print "<tr>\n";
				print "<td align=right><input type=\"hidden\" name=\"session\"   value=\"$session\"/><input type=\"hidden\" name=\"list\"   value=\"$list\"/><input type='submit' name='visualization_step1' value='Next'/>";
				print "</td>";
			print "</tr>\n";
	print "</table>\n";		
print "</tbody></table>\n";
} # sub visualization {


sub visualization_step1 {
	my ($session, $list, $org, $viz_genes) = @_;
	my @viz_genes = @$viz_genes; 
	my $genes_size = scalar(@viz_genes);
	my $banner = &get_browse_banner("");
	print "<table cellpadding=\"0\" border=\"0\"  width=$table_width align=\"left\">\n";
		print "<tbody>";
		if (@viz_genes) {
			print "<tr>\n";
				print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Step&nbsp;2:</b></font></td>\n";
				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><br><b>Select the knowledge domains to be visualized</b></font><br><br></td>\n";
			print "</tr>\n";
			print "<tr>\n";
				print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Domain selection</b></font></td>\n";
				print "<td>";
					print "<table cellspacing='0'>\n";
#						print "<tr>\n";
#							print "<td align=right><input type='submit' name='visualization_step' value='Next'/><input type='hidden' name='org' value=\"$org\" />";
#							print "</td>";
#						print "</tr>\n";	

						print "<tr>\n";
							print "<td>";
								print "<table border=0 cellspacing='1'>\n";
					 print "<tr>\n";
						print "<td class=biocompendium_header><b>Select <input type=\"button\" name=\"CheckAll\" value=\"All\" onClick=\"checkAll(document.biocompendium_visualization.viz_domain)\"><input type=\"button\" name=\"UnCheckAll\" value=\"None\" onClick=\"uncheckAll(document.biocompendium_visualization.viz_domain)\"></b></td>\n";
						print "<td class=biocompendium_header><b>Knowledge domain</b></td>\n";
					print "</tr><tbody>\n";
					my $i = 0;
					my $bg;
	#				my @domains = qw(Pathways GO Chemicals Drugs Ligands Metabolites Diseases);  
#					my @domains = qw(Pathways GO Diseases);  
					my @domains = qw(Pathways Diseases);  
					foreach my $domain (@domains) {
						$i++;
						if($i%2==0) {
							$bg="#D4EDF4";
						}
						else {
							$bg="#cfc3f3";
						}
							print "<tr bgcolor=\"$bg\">\n";
								print "<td width=5% align=center><font face=\"Arial\" size=\"2\" color=\"#000000\"><INPUT TYPE=\"checkbox\" NAME=\"viz_domain\" VALUE=\"$domain\"></font></td>\n";
								print "<td width=95%><font face=\"Arial\" size=\"2\" color=\"#000000\">$domain</font></td>\n";
							print "</tr>\n";
					} # foreach my $domain (@domains) {

# chemistry stuff
					$i++;
          if($i%2==0) {
            $bg="#D4EDF4";
          }
          else {
            $bg="#cfc3f3";
          }
            print "<tr bgcolor=\"$bg\">\n";
              print "<td width=5% align=center><font face=\"Arial\" size=\"2\" color=\"#000000\"></font></td>\n";
              print "<td width=95%><font face=\"Arial\" size=\"2\" color=\"#000000\">Chemicals";
								print "<table>";
									print "<tr>";
										print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><INPUT TYPE=\"checkbox\" NAME=\"viz_domain\" VALUE=\"Drugs\">Drugs</font></td>";
									print "</tr>";
									print "<tr>";
										print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><INPUT TYPE=\"checkbox\" NAME=\"viz_domain\" VALUE=\"Ligands\">Ligands</font></td>";
									print "</tr>";
									print "<tr>";
										print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><INPUT TYPE=\"checkbox\" NAME=\"viz_domain\" VALUE=\"Metabolites\">Metabolites</font></td>";
									print "</tr>";
									print "<tr>";
										print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><INPUT TYPE=\"checkbox\" NAME=\"viz_domain\" VALUE=\"Other_chemicals\">Other_chemicals</font></td>";
									print "</tr>";
								print "</table>";
							print "</font></td>\n";
            print "</tr>\n";
				print "</tbody></table>\n";
			print "</tr>\n";
			print "</tbody></table></tr>\n";

			print "<tr>\n";
				print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Step&nbsp;3:</b></font></td>\n";
				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><br><b>Select the visualization module (tool) to be used</b></font><br><br></td>\n";
			print "</tr>\n";	
			print "<tr>\n";
				print "<td class=light_blue><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Tool selection</b></font></td>\n";
					print "<td>";
						print "<table cellspacing='0'>\n";
							print "<tr>\n";
								print "<td class=biocompendium><input type='radio' name='viz_tool' value='Medusa' checked><a class=biocompendium href=\"http://sourceforge.net/projects/graph-medusa/\"><b>Medusa</b></a></td>";
								print "<td class=biocompendium> - 2D visualization tool</td>";
							print "</tr>\n";
							print "<tr>\n";
								print "<td class=biocompendium><input type='radio' name='viz_tool' value='Arena3d'><a class=biocompendium href=\"http://arena3d.org/\"><b>Arena3D</b></a></td>";
								print "<td class=biocompendium> - 3D visualization tool</td>";
							print "</tr>\n";
						print "</table>";	
				print "</td>";
			print "<tr>\n";

							my $spaces = "&nbsp" x 50;
							print "<tr>\n";
								print "<td class=light_blue><br></td>\n";
								print "<td align=left>$spaces<input type='submit' name='visualization_step2' value='Next'/><input type=\"hidden\" name=\"session\"   value=\"$session\"/><input type=\"hidden\" name=\"list\"   value=\"$list\"/><input type='hidden' name='org' value=\"$org\" />";
								my $viz_genes_str = join("\n", @viz_genes);
								print "<input type='hidden' name='viz_genes_str' value=\"$viz_genes_str\" /></td>";
							print "</tr>\n";	
		} # if (@viz_genes) {
		else {
			print "<tr>\n";
				print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></font></td>\n";
				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><br><b>No genes selected for visualization, go back and select the genes</b></font><br><br></td>\n";
			print "</tr>\n";
		}
		print "</tbody>";
	print "</table>";
} # sub visualization_step1 {

sub visualization_step2 {
	my ($session, $list, $org, $viz_genes_str, $viz_domains, $viz_tool) = @_;
	my @viz_genes = split("\n", $viz_genes_str); 
	my @viz_domains = @$viz_domains; 
	my $banner = &get_browse_banner("");
	print "<table cellpadding=\"0\" border=\"0\"  width=$table_width align=\"left\">\n";
		print "<tbody>";
		if (@viz_domains) {
			print "<tr>\n";
				print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></font></td>\n";
				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><br><b>Visualization of selected genes and domains in $viz_tool</b></font><br><br></td>\n";
			print "</tr>\n";
				my $call_viz_tool = "";
				if ($viz_tool eq "Medusa") {
					 $call_viz_tool = &medusa($org, \@viz_genes, \@viz_domains);
				} 
				else {
					 $call_viz_tool = &arena3d_call($session, $list, $org, \@viz_genes, \@viz_domains);
				}
		}
		else {
			print "<tr>\n";
				print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Description</b></font></td>\n";
				print "<td><font face=\"Arial\" size=\"2\" color=\"#000000\"><br><b>No knowledge domains selected for visualization, go back and select the domains</b></font><br><br></td>\n";
			print "</tr>\n";
		}
} # sub visualization_step2 {			

sub arena3d_call {
	my ($session, $list, $org, $viz_genes, $viz_domains) = @_;
use DbLink;	
	my $file_name = "sessions/" . $session . "/" .  $list . "_arena3d.txt";
	my $file = $outPutDir . $file_name;
	system("rm -f $file");

my $table_width = 1200;
  print "<table cellpadding=\"10\" border=\"0\"  width=$table_width>\n";
                print "<tbody>";

  unless (-e $file) {
                my $generated_arena3d_input_file = &arena3d($file, $org, $viz_genes, $viz_domains);
        } #  unless (-e $file) {


	if (-e $file) {
		close(FH);
		open(FH, $file);
		my @lines = <FH>;	
		close(FH);
		my $no_lines = @lines;	
		
		if ($no_lines > 10) {
                	print "<tr>\n";
                        	print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Arena3D input file</b></font></td>\n";
                        	print "<td><a href=\"/cgi-bin/download.cgi?arena3d_file=$file_name\"><b>Download</a> input file for visualizaton of selected genes and knowledge domains in <a href=\"http://arena3d.org\" target=\"_blank\">Arena3D</a></b>\n";
                        	print "<br></td>\n";
                	print "</tr>\n";
		} # if ($no_lines > 10)
		else {
                	print "<tr>\n";
                        	print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Arena3D input file</b></font></td>\n";
                        	print "<td><b>No interaction information available for given data set!!!<b>\n";
                        	print "<br></td>\n";
                	print "</tr>\n";
		}
	} # if (-e $file) {
                print "</tbody>";
	print "</table>";	
	
} # sub arena3d_call {

sub arena3d {
	my ($file, $org, $viz_genes, $viz_domains) = @_;
	use DbLink;
  my @viz_genes = @$viz_genes;
  my @viz_domains = @$viz_domains;

  my $edges = "";
  my $nodes = "";
	
	my $gene_nodes = "";
	my $pathway_nodes = "";
	my $disease_nodes = "";
	my $drug_nodes = "";
	my $ligand_nodes = "";
	my $metabolite_nodes = "";
	my $other_chemical_nodes = "";

	my @gene_nodes = ();
	my @pathway_nodes = ();
	my @disease_nodes = ();
	my @drug_nodes = ();
	my @ligand_nodes = ();
	my @metabolite_nodes = ();
	my @other_chemical_nodes = ();

	my $at_least_one_node_gene = "no";
	my $at_least_one_node_pathway = "no";
	my $at_least_one_node_disease = "no";
	my $at_least_one_node_drug = "no";
	my $at_least_one_node_ligand = "no";
	my $at_least_one_node_metabolite = "no";
	my $at_least_one_node_other_chemical = "no";

	my $chem_at_least_one_node_drug = "no";
	my $chem_at_least_one_node_ligand = "no";
	my $chem_at_least_one_node_metabolite = "no";
	my $chem_at_least_one_node_other_chemical = "no";

  my $drug_edges = "";
  my $metabolite_edges = "";
  my $ligand_edges = "";
 	my $other_chemical_edges = "";

	my %gene_detail_hash = ();
  foreach my $viz_genes_str (@viz_genes) {
		$at_least_one_node_gene = "yes";
    my ($gene, $gene_name, $gene_des) = split("____", $viz_genes_str);
    $gene_detail_hash{$gene}{gene_name} = $gene_name;
    $gene_detail_hash{$gene}{gene_des} = $gene_des;
		my $gene_url = "http://www.ensembl.org/$org_mappings{$org}/geneview?gene=$gene";
		$gene_nodes = "$gene_name" . "____URL::$gene_url";
		push @gene_nodes, $gene_nodes;
	} # foreach my $viz_genes_str (@viz_genes) {
  my @genes = keys %gene_detail_hash;

  my $chemistry_processed = "no";
  my %domain_hash = ();
  foreach my $viz_domain (@viz_domains) {
    $domain_hash{$viz_domain} = 1;
  }

	foreach my $viz_domain (@viz_domains) {
## pathways 
		if ($viz_domain eq "Pathways") {
			my $pathway_centric_hash = &get_pathway_kegg(\@genes, $org);
			my %pathway_centric_hash = %$pathway_centric_hash;
			foreach my $kegg_id (keys %pathway_centric_hash) {
				$at_least_one_node_pathway = "yes";
				my @ens_genes = @{$pathway_centric_hash{$kegg_id}{ens_genes}};
				my @kegg_genes = @{$pathway_centric_hash{$kegg_id}{kegg_genes}};
				my $kegg_genes_str = join("+",@kegg_genes);
				my $pathway_url = "http://www.genome.jp/dbget-bin/show_pathway?" . $kegg_id . "+" . $kegg_genes_str;
				my $pathway_description = $pathway_centric_hash{$kegg_id}{pathway_description};
				$pathway_description =~ s/ - /-/g;
				$pathway_description =~ s/ /_/g;
				$pathway_description =~ s/_$//g;
				$pathway_nodes = "$pathway_description" . "____URL::$pathway_url";
				push @pathway_nodes, $pathway_nodes;
				foreach my $gene (@ens_genes) {
					$edges .= $gene_detail_hash{$gene}{gene_name} . "::Genes\t" . $pathway_description . "::Pathways\t1\n";
				} # foreach my $gene (@ens_genes) {	
			} #foreach my $kegg_id (keys %pathway_centric_hash) {	
		} # if ($viz_domain eq "Pathways") {

## chemicals      
    elsif (($chemistry_processed eq "no") && (($viz_domain eq 'Other_chemicals')||($viz_domain eq 'Drugs')||($viz_domain eq 'Metabolites')||($viz_domain eq 'Ligands'))) {
			my $chemistry = "";
      foreach my $gene (@genes) {
        $chemistry = &get_chemistry($gene, $org);
        my %chemistry = %$chemistry;


#### drugs        
        my $drugs = $chemistry{drugs};
        my %drugs = %$drugs;
        foreach my $drug (keys %drugs) {
          my $cid = $drugs{$drug}{cid};
          if($cid) {
						$chem_at_least_one_node_drug = "yes";
            my $str = $drugs{$drug}{str};
            my $cid_link = $drugs{$drug}{cid_link};
            $drug =~ s/ /_/g;
            $drug =~ s/:|\n/-/g;
            $drug =~ s/_$//g;
            my $drug_url = $cid_link;
						$drug_nodes = "$drug" . "____URL::$drug_url";
						push @drug_nodes, $drug_nodes;
            $drug_edges .= $gene_detail_hash{$gene}{gene_name} . "::Genes\t" . $drug . "::Drugs\t1\n";
          } # if($cid) {  
        } # foreach my $drug (keys %drug_relevance) {

#### ligands
         my $ligands = $chemistry{ligands};
         my %ligands = %$ligands;
         foreach my $ligand (keys %ligands) {
           my $cid = $ligands{$ligand}{cid};
           if($cid) {
					 	$chem_at_least_one_node_ligand = "yes";
            my $str = $ligands{$ligand}{str};
            my $cid_link = $ligands{$ligand}{cid_link};
            $ligand =~ s/ /_/g;
            $ligand =~ s/:|\n/-/g;
            $ligand =~ s/_$//g;
            my $ligand_url = $cid_link;
            $ligand_nodes = $ligand . "____URL::$ligand_url";
						push @ligand_nodes, $ligand_nodes;
            $ligand_edges .= $gene_detail_hash{$gene}{gene_name} . "::Genes\t" . $ligand . "::Ligands\t1\n";
           } # if($cid) {  
         } # foreach my $ligand (keys %ligands) {

#### metabolites
        my $metabolites = $chemistry{metabolites};
        my %metabolites = %$metabolites;
        foreach my $metabolite (keys %metabolites) {
          my $cid = $metabolites{$metabolite}{cid};
          if($cid) {
						$chem_at_least_one_node_metabolite = "yes";
            my $str = $metabolites{$metabolite}{str};
            my $cid_link = $metabolites{$metabolite}{cid_link};
            $metabolite =~ s/ /_/g;
            $metabolite =~ s/:|\n/-/g;
            $metabolite =~ s/_$//g;
            my $metabolite_url = $cid_link;
            $metabolite_nodes = $metabolite . "____URL::$metabolite_url";
						push @metabolite_nodes, $metabolite_nodes;
            $metabolite_edges .= $gene_detail_hash{$gene}{gene_name} . "::Genes\t" . $metabolite . "::Metabolites\t1\n";
           } # if($cid) {  
         } # foreach my $metabolite (keys %metabolites) {

#### other chemicals
        my $other_chemicals = $chemistry{other_chemicals};
        my %other_chemicals = %$other_chemicals;
        foreach my $other_chemical (keys %other_chemicals) {
          my $cid = $other_chemicals{$other_chemical}{cid};
          if($cid) {
						$chem_at_least_one_node_other_chemical = "yes";
            my $str = $other_chemicals{$other_chemical}{str};
            my $cid_link = $other_chemicals{$other_chemical}{cid_link};
            $other_chemical =~ s/ /_/g;
            $other_chemical =~ s/:|\n/-/g;
            $other_chemical =~ s/_$//g;
            my $other_chemical_url = $cid_link;
            $other_chemical_nodes = $other_chemical . "____URL::$other_chemical_url";
						push @other_chemical_nodes, $other_chemical_nodes;
            $other_chemical_edges .= $gene_detail_hash{$gene}{gene_name} . "::Genes\t" . $other_chemical . "::Other_chemicals\t1\n";
           } # if($cid) {  
         } # foreach my $other_chemical (keys %other_chemicals) {
      }# foreach my $gene (@ens) {
			$chemistry_processed = "yes";
		} # elsif (($chemistry_processed eq "no") && (($viz_domain eq 'Chemicals')||($viz_domain eq 'Drugs')||($viz_domain eq 'Metabolites')||($viz_domain eq 'Ligands'))) {

## diseases 
    elsif ($viz_domain eq "Diseases") {
      my $disease_centric_hash = &get_diseases(\@genes, $org);
      my %disease_centric_hash = %$disease_centric_hash;
      foreach my $mim_morbid_acc (keys %disease_centric_hash) {
        $at_least_one_node_disease = "yes";
        my @ens_genes = @{$disease_centric_hash{$mim_morbid_acc}{ens_genes}};
        my $disease_url = "http://www.ncbi.nlm.nih.gov/entrez/dispomim.cgi?id=" . $mim_morbid_acc;
        my $disease_description = $disease_centric_hash{$mim_morbid_acc}{description};
        $disease_description =~ s/ - /-/g;
        $disease_description =~ s/ /_/g;
        $disease_description =~ s/_$//g;
        $disease_nodes = $disease_description . "____URL::$disease_url";
				push @disease_nodes, $disease_nodes;

        foreach my $gene (@ens_genes) {
					$edges .= $gene_detail_hash{$gene}{gene_name} . "::Genes\t" . $disease_description . "::Diseases\t1\n";
        } # foreach my $gene (@ens_genes) {
      } # foreach my $mim_morbid_acc (keys %disease_centric_hash) {
    } # elsif ($viz_domain eq "Diseases") {
	} # foreach my $viz_domain (@viz_domains) {

# chemistry is bit strange here, because what ever chemistry related domain (drug, ligand, metabolite and other chemicals) selected, other chemistry domain related
# info is calculated, so we need to take only the domains user selected 
	foreach my $viz_domain (@viz_domains) {
		if (($viz_domain eq 'Drugs') && ($chem_at_least_one_node_drug eq "yes")) {
			$edges .= $drug_edges; 
			$at_least_one_node_drug = "yes";
		}
		elsif (($viz_domain eq 'Ligands') && ($chem_at_least_one_node_ligand eq "yes")) {
			$edges .= $ligand_edges; 
			$at_least_one_node_ligand = "yes";
		}
		elsif (($viz_domain eq 'Metabolites') && ($chem_at_least_one_node_metabolite eq "yes")) {
			$edges .= $metabolite_edges; 
			$at_least_one_node_metabolite = "yes";
		}	
		elsif (($viz_domain eq 'Other_chemicals') && ($chem_at_least_one_node_other_chemical eq "yes")) {
			$edges .= $other_chemical_edges; 
			$at_least_one_node_other_chemical = "yes";
		}
	} # foreach my $viz_domain (@viz_domains) { 

	my $domains_size = scalar(@viz_domains);
	$domains_size++;

	close(FH);
	open(FH,  ">$file");
	if (($at_least_one_node_pathway eq "yes") || ($at_least_one_node_disease eq "yes") || ($at_least_one_node_drug eq "yes") || ($at_least_one_node_ligand eq "yes") || ($at_least_one_node_metabolite eq "yes") || ($at_least_one_node_other_chemical eq "yes")) { 

#		@gene_nodes = &nonRedundantList(\@gene_nodes);
#		@pathway_nodes = &nonRedundantList(\@pathway_nodes);

		print FH "#-----------------------------------\n";
		print FH "# This is the input file for Arena3D visualization tool for selected genes and knowledge domains\n";
		print FH "# Refer URL http://arena3d.org or publication \"Georgios A. Pavlopoulos, Sean I. ODonoghue, Venkata P. Satagopam,\n"; 
		print FH "# Theodoros Soldatos, Evangelos Pafilis, and Reinhard Schneider, Arena3D: Visualization of Biological Networks in 3D,\n"; 
		print FH "# BMC Systems Biology 2008, 2:104.\" for more details about Arena3D.\n";
#		print FH "# This file is generated by Venkata Satagopam (venkata.satagopam\@embl.de) from bioCompendium, part of his PhD thesis\n";
		print FH "# This file is generated by Venkata Satagopam (venkata.satagopam\@embl.de) from bioCompendium\n";
		print FH "#-----------------------------------\n";
		
		print FH "#-----------------------------------\n";
		print FH "number_of_layers::$domains_size\n";
		print FH "#-----------------------------------\n";

		print FH "#-----------------------------------\n";
		print FH "layer::Genes::clustering=true\n";
		foreach my $e (@gene_nodes) {
			$e =~ s/____URL/\tURL/g;
			$e =~ s/____CLUSTER/\tCLUSTER/g;
			print FH "$e\n";
		}
		print FH "end_of_layer_inputs\n";
		print FH "#-----------------------------------\n";

	  foreach my $viz_domain (@viz_domains) {
		## Pathways 
			    if ($viz_domain eq "Pathways") {
						print FH "#-----------------------------------\n";
						print FH "layer::Pathways::clustering=true\n";
						foreach my $e (@pathway_nodes) {
							$e =~ s/____URL/\tURL/g;
							$e =~ s/____CLUSTER/\tCLUSTER/g;
							print FH "$e\n";
						}
						print FH "end_of_layer_inputs\n";
						print FH "#-----------------------------------\n";
					} # if ($viz_domain eq "Pathways") {

    ## Diseases 
          if ($viz_domain eq "Diseases") {
            print FH "#-----------------------------------\n";
            print FH "layer::Diseases::clustering=true\n";
            foreach my $e (@disease_nodes) {
              $e =~ s/____URL/\tURL/g;
              $e =~ s/____CLUSTER/\tCLUSTER/g;
              print FH "$e\n";
            }
            print FH "end_of_layer_inputs\n";
            print FH "#-----------------------------------\n";
          } # if ($viz_domain eq "Diseases") {

    ## Drugs 
          if ($viz_domain eq "Drugs") {
            print FH "#-----------------------------------\n";
            print FH "layer::Drugs::clustering=true\n";
            foreach my $e (@drug_nodes) {
              $e =~ s/____URL/\tURL/g;
              $e =~ s/____CLUSTER/\tCLUSTER/g;
              print FH "$e\n";
            }
            print FH "end_of_layer_inputs\n";
            print FH "#-----------------------------------\n";
          } # if ($viz_domain eq "Drugs") {

    ## Ligands 
          if ($viz_domain eq "Ligands") {
            print FH "#-----------------------------------\n";
            print FH "layer::Ligands::clustering=true\n";
            foreach my $e (@ligand_nodes) {
              $e =~ s/____URL/\tURL/g;
              $e =~ s/____CLUSTER/\tCLUSTER/g;
              print FH "$e\n";
            }
            print FH "end_of_layer_inputs\n";
            print FH "#-----------------------------------\n";
          } # if ($viz_domain eq "Ligands") {

    ## Metabolites 
          if ($viz_domain eq "Metabolites") {
            print FH "#-----------------------------------\n";
            print FH "layer::Metabolites::clustering=true\n";
            foreach my $e (@metabolite_nodes) {
              $e =~ s/____URL/\tURL/g;
              $e =~ s/____CLUSTER/\tCLUSTER/g;
              print FH "$e\n";
            }
            print FH "end_of_layer_inputs\n";
            print FH "#-----------------------------------\n";
          } # if ($viz_domain eq "Metabolites") {

    ## Other chemicals 
          if ($viz_domain eq "Other_chemicals") {
            print FH "#-----------------------------------\n";
            print FH "layer::Other_chemicals::clustering=true\n";
            foreach my $e (@other_chemical_nodes) {
              $e =~ s/____URL/\tURL/g;
              $e =~ s/____CLUSTER/\tCLUSTER/g;
              print FH "$e\n";
            }
            print FH "end_of_layer_inputs\n";
            print FH "#-----------------------------------\n";
          } # if ($viz_domain eq "Other_chemicals") {
		} # foreach my $viz_domain (@viz_domains) {

    print FH "#-----------------------------------\n";
    print FH "start_connections\n";
    print FH "$edges\n";
    print FH "end_connections\n";
    print FH "#-----------------------------------\n";
	} # if (($at_least_one_node_gene eq "yes" && $at_least_one_node_pathway eq "yes").......	
	else {
		print FH "No";
	}
	close(FH);
} # sub arena3d {

sub medusa {
	my ($org, $viz_genes, $viz_domains) = @_;
use DbLink;	
	my @viz_genes = @$viz_genes;
	my @viz_domains = @$viz_domains;


	print "<tr>\n";
		print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Applet legend</b></font></td>\n";
    print "<td> 
					Genes: <img alt=\"\" src=\"/images/gene_medusa_icon.png\" border='0'><br> 
					GO: <img alt=\"\" src=\"/images/go_medusa_icon.png\" border='0'><br> 
					Pathways: <img alt=\"\" src=\"/images/pathway_medusa_icon.png\" border='0'><br> 
					Diseases: <img alt=\"\" src=\"/images/disease_medusa_icon.png\" border='0'><br> 
					Chemicals (
					Drugs: <img alt=\"\" src=\"/images/drug_medusa_icon.png\" border='0'>; 
					Ligands: <img alt=\"\" src=\"/images/ligand_medusa_icon.png\" border='0'>; 
					Metabolites: <img alt=\"\" src=\"/images/metabolite_medusa_icon.png\" border='0'>; 
					Other chemicals: <img alt=\"\" src=\"/images/chemical_medusa_icon.png\" border='0'>)<br> 
					<i> These symbols are hyperlinks</i><br></td>\n";
print "<td></td>"; # to be deleted
                print "</tr>\n";
                print "<tr>\n";
                        print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b>Applet</b></font></td>\n";
                        print "<td><br>\n";

	my $edges = "";
	my $nodes = "";
	my $n = 1;
	my $ci = 0;
	my $x = 0.5;
	my $y = 0.5;
# Pathways GO Chemicals Drugs Ligands Metabolites Diseases  
	my $gene_shape = 0; # circle
	my $pathway_shape = 1; # square
	my $go_shape = 2; # triangle
	my $chemical_shape = 3; # rhombus
	my $drug_shape = 3; # rhombus
	my $ligand_shape = 3; # rhombus
	my $metabolite_shape = 3; # rhombus
	my $other_chemical_shape = 3; # rhombus
	my $disease_shape = 4; # circle

	my $gene_color = '4,180,4';# green 
	my $pathway_color = '233,1,1'; # red
	my $go_color = "125,34,82"; # megenta
	my $chemical_color = "0,0,73"; # blue
	my $drug_color = '253,208,23'; # gold
	my $ligand_color = '48,125,126'; # cyan
	my $metabolite_color = '246,96,171'; # pink
	my $other_chemical_color = "0,0,73"; # blue
	my $disease_color = "0,0,0"; # black

	my $gene_anno = "";
	my $pathway_anno = "";
	my $drug_anno = "";
	my $ligand_anno = "";
	my $metabolite_anno = "";
	my $other_chemical_anno = "";
	my $disease_anno = "";

	my $gene_url = "";
	my $pathway_url = "";
	my $drug_url = "";
	my $ligand_url = "";
	my $metabolite_url = "";
	my $other_chemical_url = "";
	my $disease_url = "";

	my $settings = "0,0,0;100,255,100";
	my $at_least_one_node_pathway = "no";
	my $at_least_one_node_go = "no";
	my $at_least_one_node_chemical = "no";
	my $at_least_one_node_disease = "no";

	my %gene_detail_hash = ();
	foreach my $viz_genes_str (@viz_genes) {
		my ($gene, $gene_name, $gene_des) = split("____", $viz_genes_str);
		$gene_detail_hash{$gene}{gene_name} = $gene_name;
		$gene_detail_hash{$gene}{gene_des} = $gene_des;
		$gene_anno = $gene_des;
		$gene_anno =~ s/:|;/-/g; 
#		$gene_anno = quotemeta($gene_anno);
		$gene_url = "http://www.ensembl.org/$org_mappings{$org}/geneview?gene=$gene";
		$nodes .= $gene_name . ":" . $x . ":" . $y . ":" . $gene_color . ":". $gene_shape . ":" . $gene_anno . ":\'" . $gene_url . "\';\n";
		$x = 1/$n;
   	$y = 1/$n;
    $n++;
	} # foreach my $viz_genes_str (@viz_genes) {
	my @genes = keys %gene_detail_hash;


	my $chemistry_processed = "no";
	my %domain_hash = ();
	foreach my $viz_domain (@viz_domains) {
#print "viz_domain : $viz_domain<br>";	
		$domain_hash{$viz_domain} = 1;	
	}


	foreach my $viz_domain (@viz_domains) {
## pathways 
		if ($viz_domain eq "Pathways") {
			my $pathway_centric_hash = &get_pathway_kegg(\@genes, $org);
			my %pathway_centric_hash = %$pathway_centric_hash;
			foreach my $kegg_id (keys %pathway_centric_hash) {
				$at_least_one_node_pathway = "yes";
				my @ens_genes = @{$pathway_centric_hash{$kegg_id}{ens_genes}};
				my @kegg_genes = @{$pathway_centric_hash{$kegg_id}{kegg_genes}};
				my $kegg_genes_str = join("+",@kegg_genes);
				my $pathway_url = "http://www.genome.jp/dbget-bin/show_pathway?" . $kegg_id . "+" . $kegg_genes_str;
				my $pathway_description = $pathway_centric_hash{$kegg_id}{pathway_description};
				$pathway_description =~ s/ - /-/g;
				$pathway_description =~ s/ /_/g;
				$pathway_description =~ s/_$//g;
				$pathway_anno = $pathway_description;
				$nodes .= $pathway_description . ":" . $x . ":" . $y . ":" . $pathway_color . ":". $pathway_shape . ":" . $pathway_anno . ":\'" . $pathway_url . "\';\n";
				$x = 1/$n;
   			$y = 1/$n;
    		$n++;
				foreach my $gene (@ens_genes) {
					$edges .= $gene_detail_hash{$gene}{gene_name} . ":" . $pathway_description . ":1:1:1;\n";	
				} # foreach my $gene (@ens_genes) {
			} # foreach my $kegg_id (keys %pathway_centric_hash) {
		} # if ($viz_domain eq "Pathways") {			

## chemicals  		
		elsif (($chemistry_processed eq "no") && (($viz_domain eq 'Other_chemicals')||($viz_domain eq 'Drugs')||($viz_domain eq 'Metabolites')||($viz_domain eq 'Ligands'))) {
			my $drug_nodes = "";
			my $metabolite_nodes = "";
			my $ligand_nodes = "";
			my $other_chemical_nodes = "";

			my $drug_edges = "";
			my $metabolite_edges = "";
			my $ligand_edges = "";
			my $other_chemical_edges = "";

			my $chemistry = "";
			foreach my $gene (@genes) {
				$chemistry = &get_chemistry($gene, $org);	
				my %chemistry = %$chemistry;

#### drugs 				
				my $drugs = $chemistry{drugs};
				my %drugs = %$drugs;
				foreach my $drug (keys %drugs) {
					my $cid = $drugs{$drug}{cid};
					if($cid) {
						my $str = $drugs{$drug}{str};
						my $cid_link = $drugs{$drug}{cid_link};
						$drug =~ s/ /_/g;
						$drug =~ s/:|\n/-/g;
						$drug =~ s/_$//g;
						$drug_anno = $str;
						$drug_anno =~ s/ /_/g;
						$drug_anno =~ s/:|\n/-/g;
						$drug_url = $cid_link;
						$drug_nodes .= $drug . ":" . $x . ":" . $y . ":" . $drug_color . ":". $drug_shape . ":" . $drug_anno . ":\'" . $drug_url . "\';\n"; 
						$x = 1/$n;
   					$y = 1/$n;
    				$n++;
						$drug_edges .= $gene_detail_hash{$gene}{gene_name} . ":" . $drug . ":1:1:1;\n";	
					} # if($cid) {	
				} # foreach my $drug (keys %drug_relevance) {

#### ligands
				 my $ligands = $chemistry{ligands};
				 my %ligands = %$ligands;
				 foreach my $ligand (keys %ligands) {
				 	 my $cid = $ligands{$ligand}{cid};
					 if($cid) {
					 	my $str = $ligands{$ligand}{str};
						my $cid_link = $ligands{$ligand}{cid_link};
						$ligand =~ s/ /_/g;
						$ligand =~ s/:|\n/-/g;
						$ligand =~ s/_$//g;
						$ligand_anno = $str;
						$ligand_anno =~ s/ /_/g;
						$ligand_url = $cid_link;
						$ligand_nodes .= $ligand . ":" . $x . ":" . $y . ":" . $ligand_color . ":". $ligand_shape . ":" . $ligand_anno . ":\'" . $ligand_url . "\';\n"; 
						$x = 1/$n;
   					$y = 1/$n;
    				$n++;
						$ligand_edges .= $gene_detail_hash{$gene}{gene_name} . ":" . $ligand . ":1:1:1;\n";	
					 } # if($cid) {  
				 } # foreach my $ligand (keys %ligands) {

#### metabolites
				my $metabolites = $chemistry{metabolites};
				my %metabolites = %$metabolites;
				foreach my $metabolite (keys %metabolites) {
					my $cid = $metabolites{$metabolite}{cid};
					if($cid) {
						my $str = $metabolites{$metabolite}{str};
						my $cid_link = $metabolites{$metabolite}{cid_link};
						$metabolite =~ s/ /_/g;
						$metabolite =~ s/:|\n/-/g;
						$metabolite =~ s/_$//g;
						$metabolite_anno = $str;
						$metabolite_anno =~ s/ /_/g;
						$metabolite_anno =~ s/:|\n/-/g;
						$metabolite_url = $cid_link;
						$metabolite_nodes .= $metabolite . ":" . $x . ":" . $y . ":" . $metabolite_color . ":". $metabolite_shape . ":" . $metabolite_anno . ":\'" . $metabolite_url . "\';\n"; 
						$x = 1/$n;
   					$y = 1/$n;
    				$n++;
						$metabolite_edges .= $gene_detail_hash{$gene}{gene_name} . ":" . $metabolite . ":1:1:1;\n";	
					 } # if($cid) {  
				 } # foreach my $metabolite (keys %metabolites) {

#### other chemicals
				my $other_chemicals = $chemistry{other_chemicals};
				my %other_chemicals = %$other_chemicals;
				foreach my $other_chemical (keys %other_chemicals) {
					my $cid = $other_chemicals{$other_chemical}{cid};
					if($cid) {
						my $str = $other_chemicals{$other_chemical}{str};
						my $cid_link = $other_chemicals{$other_chemical}{cid_link};
						$other_chemical =~ s/ /_/g;
						$other_chemical =~ s/:|\n/-/g;
						$other_chemical =~ s/_$//g;
						$other_chemical_anno = $str;
						$other_chemical_anno =~ s/ /_/g;
						$other_chemical_url = $cid_link;
						$other_chemical_nodes .= $other_chemical . ":" . $x . ":" . $y . ":" . $other_chemical_color . ":". $other_chemical_shape . ":" . $other_chemical_anno . ":\'" . $other_chemical_url . "\';\n"; 
						$x = 1/$n;
   					$y = 1/$n;
    				$n++;
						$other_chemical_edges .= $gene_detail_hash{$gene}{gene_name} . ":" . $other_chemical . ":1:1:1;\n";	
					 } # if($cid) {  
				 } # foreach my $other_chemical (keys %other_chemicals) {
			}# foreach my $gene (@ens) {

			if($chemistry_processed eq "no" && $domain_hash{'Drugs'}) {
				$nodes .= $drug_nodes;
				$edges .= $drug_edges;
				$at_least_one_node_chemical = "yes";
			} # elsif($chemistry_processed eq "no" && $domain_hash{'Drugs'}) {
			elsif($chemistry_processed eq "no" && $domain_hash{'Ligands'}) {
				$nodes .= $ligand_nodes;
				$edges .= $ligand_edges;
				$at_least_one_node_chemical = "yes";
			} # elsif($chemistry_processed eq "no" && $domain_hash{'Ligands'}) {
			elsif($chemistry_processed eq "no" && $domain_hash{'Metabolites'}) {
				$nodes .= $metabolite_nodes;
				$edges .= $metabolite_edges;
				$at_least_one_node_chemical = "yes";
			} # elsif($chemistry_processed eq "no" && $domain_hash{'Metabolites'}) {
			elsif ($domain_hash{'Other_chemicals'}) {
				$nodes .= $other_chemical_nodes; 
				$edges .= $other_chemical_edges;
				$at_least_one_node_chemical = "yes";
			} # if ($domain_hash{'Chemicals'}) {
			$chemistry_processed = "yes";
		} # elsif (($chemistry_processed eq "no") && (($viz_domain eq 'Other_chemicals')||($viz_domain eq 'Drugs')||($viz_domain eq 'Metabolites')||($viz_domain eq 'Ligands'))) {

## diseases 
    elsif ($viz_domain eq "Diseases") {
      my $disease_centric_hash = &get_diseases(\@genes, $org);
      my %disease_centric_hash = %$disease_centric_hash;
      foreach my $mim_morbid_acc (keys %disease_centric_hash) {
        $at_least_one_node_disease = "yes";
        my @ens_genes = @{$disease_centric_hash{$mim_morbid_acc}{ens_genes}};
        my $disease_url = "http://www.ncbi.nlm.nih.gov/entrez/dispomim.cgi?id=" . $mim_morbid_acc;
        my $disease_description = $disease_centric_hash{$mim_morbid_acc}{description};
        $disease_description =~ s/ - /-/g;
        $disease_description =~ s/ /_/g;
        $disease_description =~ s/_$//g;
        $disease_anno = $disease_description;
        $nodes .= $disease_description . ":" . $x . ":" . $y . ":" . $disease_color . ":". $disease_shape . ":" . $disease_anno . ":\'" . $disease_url . "\';\n";
        $x = 1/$n;
        $y = 1/$n;
        $n++;
        foreach my $gene (@ens_genes) {
          $edges .= $gene_detail_hash{$gene}{gene_name} . ":" . $disease_description . ":1:1:1;\n";
        } # foreach my $gene (@ens_genes) {
      } # foreach my $mim_morbid_acc (keys %disease_centric_hash) {
    } # elsif ($viz_domain eq "Diseases") {
	} #foreach my $viz_domain (@viz_domains) { 

	if ($at_least_one_node_pathway eq "yes" || $at_least_one_node_chemical eq "yes" || $at_least_one_node_disease eq "yes") {
		print "<applet code=\"medusa.applet.MedusaLite.class\" archive=\"/medusa/Medusa.jar\" height=\"600\" width=\"1000\">\n";
		print "<param name=\"settings\" value=\"$settings\">\n";
		print "<param name=\"edges\" value=\"$edges\">\n";
		print "<param name=\"nodes\" value=\"$nodes\">\n";
		print "<param name=\"X\" value=\"500\"><param name=\"Y\" value=\"500\">\n";
		print "<param name=\"layout\" value=\"true\">\n";
	}
	else {
		print "<b>No interaction information available for given data set!!!<b>";
	}	
                        print "<br></td>\n";
                print "</tr>\n";
                print "<tr>\n";
                        print "<td class=light_blue width=12><font face=\"Arial\" size=\"2\" color=\"#000000\"><b></b></font></td>\n";
                        print "<td><br><br><br></td>\n";
                print "<tr>\n";
                print "</tbody>";
	print "</table>";	
} # sub medusa

sub get_diseases {
  my ($genes, $org) = @_;
  my @genes = @$genes;
  my %disease_centric_hash = ();
  foreach my $gene (@genes) {
    my $disease_result = &DbLink::GetDiseaseForGene($gene, $org);
    my %disease_result = %$disease_result;
    my $description = "";
    foreach my $mim_morbid_acc (keys %disease_result) {
      $description = $disease_result{$mim_morbid_acc}{description};
			push @{$disease_centric_hash{$mim_morbid_acc}{ens_genes}}, $gene;
      $disease_centric_hash{$mim_morbid_acc}{description} = $description;
    } # foreach my $mim_morbid_acc (keys %disease_result) {
  } # foreach my $gene (@genes) {
  return \%disease_centric_hash;
} # sub get_disease {


sub get_pathway_kegg {
	my ($genes, $org) = @_;
	my @genes = @$genes;
	my %pathway_centric_hash = ();
	foreach my $gene (@genes) {
		my $kegg_result = &DbLink::GetKeggForGene($gene, $org);
		my %kegg_result = %$kegg_result;
		my $kegg_gene = "";
		my $pathway_description = "";
		foreach my $kegg_id (keys %kegg_result) {
			$pathway_description = $kegg_result{$kegg_id}{pathway_description};
			$kegg_gene = $kegg_result{$kegg_id}{kegg_gene};
			push @{$pathway_centric_hash{$kegg_id}{ens_genes}}, $gene;
			push @{$pathway_centric_hash{$kegg_id}{kegg_genes}}, $kegg_gene;
			$pathway_centric_hash{$kegg_id}{pathway_description} = $pathway_description;
		} # foreach my $kegg_id (keys %kegg_result) {
	} # foreach my $viz_gene (@viz_genes) {
	return \%pathway_centric_hash;
} # sub get_pathway_kegg {


sub get_chemistry {
	my ($gene, $org) = @_;
use DbHumanChemicals;
use DbHumanChemicalDetails;
use DbPubchemCidSid;
use DbDrugbankCidSid;
use DbHmdbCidSid;
use DbMatador;
use DbPdbLigand;
use DbHumanSummarySheet;
use DbMouseSummarySheet;
use DbYeastSummarySheet;
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
				
				my $str = "Name=$c";
				$str .= "&Source=BioAlma";
				$str .= "&Relevance=$relevance";
	
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
		my $str = "Name=$des";
		$str   .= "&Source=DrugBank";
		$str   .= "&DrugBankID=$pk";
				
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

		my $str = "Name=$name";
		$str .= "&Source=Matador";
		$str .= "&MatadorID=$cid";

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
				my $str = "Name=$name";
		  	$str   .= "&Source=PDB";
				$str   .= "PDBID=$pdb_pk";

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
			my $str = "Name=$des";
			$str   .= "&Source=HMDB";
			$str   .= "&HMDBID=$pk";

			$metabolites{$des}{str} = $str;
	       		$metabolites{$des}{cid_link} = $cid_link;
	       		$metabolites{$des}{cid} = $cid;
		}# if($cid) {		
	} #foreach my $h (@hmdb) {

	my %result = (drugs=>\%drugs, drug_relevance=>\%drug_relevance, ligands=>\%ligands, metabolites=>\%metabolites, other_chemicals=>\%other_chemicals, other_chemical_relevance=>\%other_chemical_relevance);
	return \%result;
} # sub get_chemistry {


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
	print "<td class=\"banner_subtitle\">&nbsp;&nbsp;The compendium of biological knowledge</td>"; 
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

