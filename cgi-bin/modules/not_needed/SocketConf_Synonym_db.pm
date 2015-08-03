package SocketConf_Synonym_db;
						         
sub getSocketConf {
#	my $HOST = "10.1.1.154";	
#	my $HOST = "10.1.1.145";	
	my $HOST = "localhost";	
	my $PORT = 77779;	

	my $END_OF_MESSAGE_TAG = "_END_OF_MESSAGE_";
	my %conf = (HOST=>$HOST, PORT=>$PORT, END_OF_MESSAGE_TAG=>$END_OF_MESSAGE_TAG);
	return %conf;
} # sub getSocketConf {										 
1;
