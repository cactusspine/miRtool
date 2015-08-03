package hgnc_info;

sub process_genelist {
	my $gene_list_str = shift;	
use IO::Socket::INET;
use SocketConf_HGNC_Synonym_db2;

	my %result=();
	my %socket_conf = &SocketConf_HGNC_Synonym_db2::getSocketConf();

	my $method = "get_hgnc_id";
#print "gene_list_str : $gene_list_str\n<br>";
        my $msg = $method . "\n" .$gene_list_str.$socket_conf{END_OF_MESSAGE_TAG}."\n";
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
						my ($name, $hgnc2uniprot) = split("____", $e);
						my @hgnc2uniprot = split("__", $hgnc2uniprot);
						foreach my $h2p (@hgnc2uniprot) {
							my ($hgnc_id, $uniprot_acc) = split("_", $h2p);
#print "syn : $name, hgnc_id : $hgnc_id, uniprot_acc : $uniprot_acc\n<br>";
							push @{$result{$name}}, $h2p;
						}
					}
					return \%result;
} # sub process_genelists {

sub get_hgnc_annotation {
	my $gene_list_str = shift;	
use IO::Socket::INET;
use SocketConf_HGNC_Synonym_db2;

	my %result=();
	my %socket_conf = &SocketConf_HGNC_Synonym_db2::getSocketConf();

	my $method = "get_annotations_for_hgnc_id";
#print "gene_list_str : $gene_list_str\n<br>";
        my $msg = $method . "\n" .$gene_list_str.$socket_conf{END_OF_MESSAGE_TAG}."\n";
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
#print "hdb : $db - $value\n<br>";				 
						$result{$db} = $value;
					}
					return \%result;
} #sub get_hgnc_annotation
1;
