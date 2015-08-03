package uniprot_info;;

sub process_genelist {
	my $gene_list_str = shift;	
	my $org = shift;
use IO::Socket::INET;
use SocketConf_Synonym_db2;

	my %result=();
	my %socket_conf = &SocketConf_Synonym_db2::getSocketConf();

	my $method = "get_uniprot_acc";
#print "gene_list_str : $gene_list_str\n<br>";
        my $msg = $org ."\n".$method . "\n" .$gene_list_str.$socket_conf{END_OF_MESSAGE_TAG}."\n";
#print "msg : $msg<br>";

        my $clint_socket = IO::Socket::INET->new( Proto => "tcp",
                                           PeerAddr => $socket_conf{HOST},
                                           PeerPort => $socket_conf{PORT}
                                         );
        my $response = "";
        if ($gene_list_str) {
                $response = $clint_socket->send($msg);
        }
        $/ = "_END_OF_MESSAGE_";
        $response = <$clint_socket>;
        chomp($response);
        $/ = "\n";
#print "response : $response<br>";
        close($clint_socket);
	
	my @entries = split("______", $response); 
         foreach my $e (@entries) {
						my ($name, $pac_str) = split("____", $e);
#						my ($uniprot_acc, $description, $database) = split("__", $pac_str);
#print "uniprot_info ...... name : $name, pac_str : $pac_str\n<br>";
						$result{$name} = $pac_str;
					}
					return \%result;
} # sub process_genelists {

sub get_uniprot_annotation {
	my ($gene_list_str, $org, $database) = @_;
use IO::Socket::INET;
use SocketConf_Synonym_db2;

	my %result=();
	my %socket_conf = &SocketConf_Synonym_db2::getSocketConf();

	my $method = "get_annotations_for_uniprot_acc";
#print "gene_list_str : $gene_list_str\n<br>";
        my $msg = $org ."\n".$method . "\n" .$database ."\n".$gene_list_str.$socket_conf{END_OF_MESSAGE_TAG}."\n";
#print "msg : $msg<br>";

        my $clint_socket = IO::Socket::INET->new( Proto => "tcp",
                                           PeerAddr => $socket_conf{HOST},
                                           PeerPort => $socket_conf{PORT}
                                         );
        my $response = "";
        if ($gene_list_str) {
                $response = $clint_socket->send($msg);
        }
        $/ = "_END_OF_MESSAGE_";
        $response = <$clint_socket>;
        chomp($response);
        $/ = "\n";
#print "response : $response<br>";
        close($clint_socket);
	
	my @entries = split("______", $response); 
         foreach my $e (@entries) {
#print "e : $e\n<br>";				 
						my ($db, $value) = split("____", $e);
#print "db : $db - $value\n<br>";				 
						$result{$db} = $value;
					}
					return \%result;
} # sub get_uniprot_annotation {
1;
