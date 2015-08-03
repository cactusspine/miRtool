#!/usr/bin/perl -wT

use CGI ':standard';
use CGI::Carp qw(fatalsToBrowser); 

my $files_location; 
my $arena3d_file; 
my @fileholder;
#my $log_file;
	my $outPutDir = "/home/database/projects/gist/httpd/htdocs/mirna/database/temp/";
	$files_location = $outPutDir . "sessions/";
#	$log_file = "$files_location" . "arena3d.log";

	$arena3d_file = param('file');
	#$arena3d_file will be sthi like $session.'/query_output.txt'
	if ($arena3d_file eq '') { 
		print "Content-type: text/html\n\n"; 
		print "You must specify a file to download."; 
	} else {

		open(DLFILE, "<$files_location/$arena3d_file") || Error('open', 'file'); 
		@fileholder = <DLFILE>; 
		close (DLFILE) || Error ('close', 'file'); 

#		open (LOG, ">>$log_file") || Error('open', 'log_file');
#		print LOG "$arena3d_file\n";
#		close (LOG);

		print "Content-Type:application/x-download\n"; 
		print "Content-Disposition:attachment;filename=$arena3d_file\n\n";
		print @fileholder
	}

	sub Error {
      		print "Content-type: text/html\n\n";
		print "The server can't $_[0] the $_[1]: $! \n";
		exit;
	}
