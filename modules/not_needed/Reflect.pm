package Reflect;

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
	my ($input_file, $input_text, $input_type, $organism, $taxid, $output_type, $output_file_name);

	if ($input_hash{input_file}) {
		$input_file = $input_hash{input_file};
	}
	elsif ($input_hash{input_text}) {
		$input_text = $input_hash{input_text};
	}

	if ($input_hash{input_type}) {
                $input_type = $input_hash{input_type};
        }
	else {
		$input_type = "ascii_text";
	}

  if ($input_hash{organism}) {
		 my $organism_taxid_or_name = $input_hash{organism};
		 $taxid = $organism_taxid_or_name; 
		$organism = &stringSpecies::getStringSpecies($organism_taxid_or_name);
        }
	else {
		$organism = "Homo sapiens";
	}

	if ($input_hash{output_type}){
		$output_type = $input_hash{output_type};
	}
#print "input_file : $input_file, input_type : $input_type, organism : $organism, output_type : $output_type\n"; 
        my $content = "";
        if ($input_type eq "ascii_text") {
                $content = $input_text;
        }
        elsif ($input_type eq "ascii_file") {
                if(open(ASCII_FILE, $input_file)||die "can't open ascii_file : $input_file"){
                        while (<ASCII_FILE>){
                                $content .= $_;
                        }
                }
        }

	if ($output_type eq 'html') {
	        if ($input_hash{output_file_name}){
        	        $output_file_name = $input_hash{output_file_name};
        	}
		else {
			if ($input_file) {
			        if ($input_file=~m/^.*(\\|\/)(.*)/){ # strip the remote path and keep the file_name 
        	        		$output_file_name= $2;
			        }
			        else {
                			$output_file_name = $input_file;
        			}
			}
			else {
				my $date = `date +%k%M%S%N`;
			        $date =~ s/ //g;
			        chop($date);
			        $output_file_name = $date;
			}
		        my @of = split('\.', $output_file_name);
		        $output_file_name = $of[0];
		}

		if ($input_type eq "ascii_text" || $input_type eq "ascii_file") {
       			$output_file_name = $output_file_name . "_reflected.html";
			my $reflected_content = &reflect_service($content, $organism, $input_type);
			my $reflect_js = &reflect_js();
			close(FH);
			open(FH, ">$output_file_name");
			print FH "<html><title>Reflect</tible><head>$reflect_js</head><body>$reflected_content</body></html>";
			close(FH);
		}
		else {
			$output_file_name = $output_file_name . "_reflected.tar";
			my $call_on_the_fly_service = &on_the_fly_service($input_file, $organism, $output_file_name);
		}
		
	}
        else {
                $content = &conversion_service($input_file, $input_type);
#print STDERR "content :$content<br>";
#        	my $reflected_content = &reflect_service($content, $organism, $input_type);
#        	my $reflected_content = &reflect_REST_GetHTML('GetHTML', $content, $taxid);
        	my $reflected_content = &reflect_REST_GetEntities('GetEntities', $content, $taxid);
#print STDERR "reflected_content :$reflected_content<br>";

#	        my $parsed_reflected_content = &parse_reflected_content($reflected_content, $organism, $taxid);
#	        my $parsed_reflected_content = &parse_REST_reflected_content($reflected_content, $organism, $taxid);
	        my $parsed_reflected_content = &parse_REST_tsv_reflected_content($reflected_content, $organism, $taxid);
#	       	my %proteins = %{%$parsed_reflected_content->{proteins}};
#	       	my %chemicals = %{%$parsed_reflected_content->{chemicals}};
#
#		foreach my $p (sort {$proteins{$a} cmp $proteins{$b}} keys %proteins) {
##		        my $description = &stitchAPI::getDescription($p);       
#			print "p : $p, name : $proteins{$p}\n";
##			print "p : $p, name : $proteins{$p}, des : $description\n";
#		}
		return $parsed_reflected_content;
	}
}

sub conversion_service {
	my ($input_file, $input_type) = @_;
	my $conversion_service = "http://biocompendium.embl.de/cgi-bin/conversion_service.cgi?";
	my $ua = LWP::UserAgent->new();
	my $req = POST $conversion_service,
	Content_Type => 'form-data',
	Content => [
        	fname => [ $input_file ],
	        ftype => $input_type,
	];
	my $response = $ua->request($req);
	my $content_url = "";
	if ($response->is_success()) {
        	$content_url = $response->content;
	} else {
        	print $response->as_string;
	}
	my @content_url = split("\n", $content_url);
	my @grep_content_url = grep(/conversionService\/upload/, @content_url);
        my $file_url = $grep_content_url[0]; 
        my $content = get($file_url);
	$content =~ s/"|'/ /g;
#print STDERR "<br>content : $content\n<br>";
	return $content;
} # sub conversion_service {

sub reflect_service {
	my ($message, $organism, $input_type) = @_;
print "message : $message<br>";	
print "organism : $organism<br>";	
print "organism : $organism<br>";	
  my $reflected_content = "";
	if ($input_type eq 'URL') {
		my $reflect_url = "http://reflect.ws/ReflectPage?url=" . $message . "&org=" . $organism; 
		$reflected_content = get($reflect_url);
	}
	else {
	        my $reflect_servelet = "http://reflect.ws/ReflectServlet";
	        my $currentPageURL = "http://schneider-www.embl.de/schneider/VS-folder";
        	my $reflect_ua = LWP::UserAgent->new();
	        my $reflect_req = POST $reflect_servelet,
				Content => [
                			message =>  $message,
		        	        organism => $organism,
        		        	currentPageURL => $currentPageURL,
		        	];
        	my $reflect_response = $reflect_ua->request($reflect_req);
        	if ($reflect_response->is_success()) {
                	$reflected_content = $reflect_response->content;
	        } else {
        	        print $reflect_response->as_string;
        	}
	}
	return $reflected_content;
} # sub reflected_content { 

# Reflect a text/webpage
sub reflect_Text {
  use LWP::UserAgent;
  use URI::Escape;

  my $text = shift;
  $text = uri_escape($text);

  #organism: should be the name of it occuring in the NCBI TaxIDs
  my $organism = uri_escape("Homo sapiens");

  #prepare Client
  my $postRequest = LWP::UserAgent->new;
  $postRequest->timeout(2);
  $postRequest->agent('Mozilla/4.0');

  #make request
  my $request = HTTP::Request->new(POST => 'http://reflect.ws/ReflectServlet');
  $request->content_type('application/x-www-form-urlencoded');
  $request->header(
    Accept => 'application/atom+xml,application/xml,text/xml',
    Connection => 'close',
    mime_type => 'text/html'
  );
  $request->content("message=".$text."&organism=".$organism);

  my $response = $postRequest->request($request);
  $response = $response->content;

  return $response;
}

sub reflect_REST_GetEntities {
  use LWP::UserAgent;
  use URI::Escape;

  my $function = shift;
  my $text = shift;
	my $taxid = shift;
	$text =~ s/\n/ /g;
#	$text =~ s/[^[:ascii:]]+//g;
#print STDERR "text : $text<br>";
#print STDERR "taxid : $taxid<br>";
#$text="nr1h2";
#$text="P04637 Q12888 Q13625";
# $text = uri_escape($text);

 $text = uri_escape_utf8($text);
#print STDERR "text : $text<br>";
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


#Reflect a String via the REST interface
sub reflect_REST_GetHTML {
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
  $request->content("document=".$text."&entity_types=".$entity);

  my $reflected_content = "";
  my $reflect_response = $postRequest->request($request);
  if ($reflect_response->is_success()) {
     	$reflected_content = $reflect_response->content;
	} else {
      print $reflect_response->as_string;
  }

  return $reflected_content;
} #sub reflect_REST_GetHTML

sub parse_REST_tsv_reflected_content {
        my ($content, $organism, $taxon) = @_;
				my @content = split('\n', $content);
#print STDERR "content : @content<br>--------------------";
        my @proteins = ();
        foreach my $bioentity_line (@content) {
#print STDERR "content : $bioentity_line\n<br>--------------------";
					my ($name, $reflect_tax_id, $bioentity_id) = split("\t", $bioentity_line);
					if ($taxon == $reflect_tax_id) {
print STDERR "bioentity_id : $bioentity_id\n<br>--------------------";
						push @proteins, $bioentity_id;
					}
        } # foreach my $bioentity_line (@bioentities) {
        return \@proteins;
} # sub parse_REST_tsv_reflected_content {

sub parse_REST_reflected_content {
        my ($content, $organism, $taxon) = @_;
				my @content = split('<span', $content);
#print STDERR "content : @content<br>--------------------";
        my @bioentities = grep("name", @content);
#print "bioentities : @bioentities<br>";
        my @proteins = ();
#        my %chemicals = ();
        foreach my $bioentity_line (@bioentities) {
#print STDERR "content : $bioentity_line\n<br>--------------------";
# ='reflectEntity0'>9606.ENSP00000231790</span>
# ='reflectEntity0' name='9606.ENSP00000231790'></span>
#                if ($bioentity_line =~ /='reflectEntity\d+'>(.*)<\/span>/) {
                if ($bioentity_line =~ /name='.*'>(.*)<\/span>/) {
	                my $bioentity_ids = $1;
#print STDERR "bioentity_ids : $bioentity_ids\n<br>";
									my @bioentity_ids = split(";", $bioentity_ids);
									push @proteins, @bioentity_ids;
                } # if ($bioentity_line =~ /.*\('(.*)','','', 50\).*>(.*)<\/a>.*/) {
        } # foreach my $bioentity_line (@bioentities) {
        return \@proteins;
} # sub parse_REST_reflected_content {

sub parse_reflected_content {
        my ($content, $organism, $taxon) = @_;
        my @bioentities = split("reflect_", $content);
        my %proteins = ();
        my %chemicals = ();
        foreach my $bioentity_line (@bioentities) {
                if ($bioentity_line =~ /.*\('(.*)','','', 50\).*>(.*)<\/a>.*/) {
                        my $bioentity_id = $1;
                        my $bioentity_name = $2;
                        my @bioentity_ids = split('\+', $bioentity_id);
                        foreach my $bid (@bioentity_ids) {
                                # if the bioentity id starts with '-1.' it is chemical eg : "-1.CID000001003"  
                                if ($bid =~ '-1.') {
                                        $bid =~ s/-1\.//g;
                                        $chemicals{$bid} = $bioentity_name;
                                }
                                else {
                                        $proteins{$bid} = $bioentity_name;
                                }
                                # incluse disease secton here
                        } # foreach my $bid (@bioentity_ids) {
                } # if ($bioentity_line =~ /.*\('(.*)','','', 50\).*>(.*)<\/a>.*/) {
        } # foreach my $bioentity_line (@bioentities) {
        my %result = (proteins=>\%proteins, chemicals=>\%chemicals);
        return \%result;
} # sub parse_reflected_content {

sub on_the_fly_service {
        my ($input_file, $organism, $output_file_name) = @_;
        my $conversion_service = "http://vschneider01.embl.de/converterService/Converter?";
        my $ua = LWP::UserAgent->new();
        my $req = POST $conversion_service,
        Content_Type => 'form-data',
        Content => [
                mptest =>  [ $input_file ],
                organism => $organism,
        ];

        my $response = $ua->request($req);
        my $content_url = "";
        if ($response->is_success()) {
                $content_url = $response->content;
        } else {
                print $response->as_string;
        }
        chop($content_url);
	my $tarball_url = $content_url;
        $tarball_url =~ s/_final.html/_files_tarball.tar/;
	getstore($tarball_url, $output_file_name);
        my $date = `date +%k%M%S%N`;
        $date =~ s/ //g;
       	chop($date);
        my $tmp_dir = "tmp_" . $date;
        `mkdir $tmp_dir; mv $output_file_name $tmp_dir; cd $tmp_dir; tar -xvf $output_file_name; chmod +x *; rm -f $output_file_name; tar -cvf  $output_file_name *; mv $output_file_name ../.; cd ..; rm -rf $tmp_dir;`;
} #

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
