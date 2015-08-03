package Reflect_Synonym_db;

use strict;
use stringSpecies;
use stitchAPI;
use LWP::Simple;
use HTTP::Request::Common;
use LWP::UserAgent;	
use File::Basename;

sub get_reflected_bioentities {
	my %input_hash = @_;
#print "<br>srk srk srk --------------------<br>";
	my $input_text = $input_hash{input_text};
	my $input_type = $input_hash{ascii_text};

	my $taxid;
	my $organism;
  if ($input_hash{organism}) {
		 my $organism_taxid_or_name = $input_hash{organism};
		 $taxid = $organism_taxid_or_name; 
		$organism = &stringSpecies::getStringSpecies($organism_taxid_or_name);
        }
	else {
		$organism = "Homo sapiens";
	}

          my $content = $input_text;
        	my $reflected_content = &reflect_REST_GetEntities('GetEntities', $content, $taxid);

#	        my $parsed_reflected_content = &parse_REST_tsv_reflected_content($reflected_content, $organism, $taxid);
#		return $parsed_reflected_content;
	return $reflected_content;
}

sub reflect_REST_GetEntities {
  use LWP::UserAgent;
  use URI::Escape;

  my $function = shift;
  my $text = shift;
	my $taxid = shift;
#print STDERR "taxid : $taxid<br>";
  $text = uri_escape($text);

#  my $entity = uri_escape("$taxid -1");
  my $entity = uri_escape("$taxid");

  #prepare Client
  my $postRequest = LWP::UserAgent->new;
#  $postRequest->timeout(2);
#  $postRequest->agent('Mozilla/4.0');

  #make request
  my $request = HTTP::Request->new(POST => 'http://reflect.cbs.dtu.dk/REST/'.$function);
  $request->content_type('application/x-www-form-urlencoded');
  $request->header(
    Accept => 'application/atom+xml,application/xml,text/xml',
    Connection => 'close',
    mime_type => 'text/html'
  );
  $request->content("document=".$text."&entity_types=".$entity."&format=tsv");

  my $reflected_content = "";
  my $reflect_response = $postRequest->request($request);
  if ($reflect_response->is_success()) {
     	$reflected_content = $reflect_response->content;
	} else {
      print $reflect_response->as_string;
  }

  return $reflected_content;
} #sub reflect_REST_GetEntities


sub parse_REST_tsv_reflected_content {
        my ($content, $organism, $taxon) = @_;
				my @content = split('\n', $content);
#print STDERR "content : @content<br>--------------------";
        my @proteins = ();
        foreach my $bioentity_line (@content) {
#print STDERR "content : $bioentity_line\n<br>--------------------";
					my ($name, $reflect_tax_id, $bioentity_id) = split("\t", $bioentity_line);
					if ($taxon == $reflect_tax_id) {
#print STDERR "bioentity_id : $bioentity_id\n<br>--------------------";
						push @proteins, $bioentity_id;
					}
        } # foreach my $bioentity_line (@bioentities) {
        return \@proteins;
} # sub parse_REST_tsv_reflected_content {


sub reflect_js {
	my $reflect_js = '<script type="text/javascript" src="http://reflect.ws/script/reflect_popup.js"></script>
<script type="text/javascript" src="http://reflect.ws/script/reflect_overlib_4.23.js"></script>
<script type="text/javascript" src="http://reflect.ws/script/reflect_overlib_draggable.js"></script>
<script type="text/javascript" src="http://reflect.ws/script/reflect_overlib_anchor.js"></script>
<script type="text/javascript" src="http://reflect.ws/script/reflect_escHandler.js"></script>
<link rel="Stylesheet" href="http://reflect.ws/style/Popup.css" type="text/css">';
	return $reflect_js;
}

1;
