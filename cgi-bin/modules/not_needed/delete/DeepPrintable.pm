package DeepPrintable;

use strict;
=head1  DeepPrintable

    Base class supporting recursive printing of the attributes of nested objects

    Method "deepPrintable" maps the instance variables of the current object 
    and, recursively, of all objects derived from "DeepPrintable" onto a 
    regular HASH.  Simple types and list types (ARRAY, HASH) are structurally
    conserved.  

    Author: Bernhard

=cut

use Data::VarPrint;

use constant IsDeepPrintable__ => 1;

=head1 new

  Purpose:        constructor
  Prototype:
                  $this = new >>SubClass<<
  Input:
                  <NONE>
  Output:
                  object of type >>SubClass<<

=cut

sub new {
    my $class = shift;
    my $this = {};
    $this->{'isDeepPrintable'} = IsDeepPrintable__;
    bless($this, $class);
    $this;
}

=head1 deepPrint

  Purpose:        print the structurally equivalent HASH of $this
  Prototype:
                  $this->deepPrint()
  Input:
                  <NONE>
  Output:
                  prints to STDOUT

=cut

sub deepPrint {
    my $this = shift;
    print "<<$this>> => ";
    VarPrint($this->_getDeepPrintable());
}

=head1 deepPrintable

  Purpose:        return the structurally equivalent HASH of $this
  Prototype:
                  $printable = $this->deepPrintable()
  Input:
                  <NONE>
  Output:
                  $printable  <HASH>  

=cut 

sub deepPrintable {
    shift->_getDeepPrintable();
}

sub _getDeepPrintable {
    my $this = shift;
    my $recursionCache = shift;

    $recursionCache->{$this} = 1;
    my $out = {};
    foreach my $attr (keys %$this) {
	next if $attr eq 'isDeepPrintable';
	$out->{$attr} = _getDeepPrintableForAttribute($this->{$attr}, $recursionCache);
    }
    $out;
}

sub _getDeepPrintableForAttribute {
    my $var = shift;
    my $recursionCache = shift;

    my $type = ref $var;

    my $printable;
    if      ($type eq '')      {
	$printable = $var;
    } elsif ($type eq 'HASH')  {
	$printable = _getDeepPrintable($var, $recursionCache);
    } elsif ($type eq 'ARRAY') {
	$printable = [];
	foreach (@$var) {
	    push @$printable, _getDeepPrintableForAttribute($_, $recursionCache);
	}
    } elsif ($type eq 'CODE')   {
	$printable = "$var";
    } else {
	if ($var->{isDeepPrintable}) {
	    if ($recursionCache->{$var}) {
		$printable = {"<<$var>>" => "RECURRENT"};
	    } else {
		$printable = {"<<$var>>" => $var->_getDeepPrintable($recursionCache)};
	    }
	} else {
	    $printable = {"<<$var>>" => $var};
	}
    }
    $printable;
}

1;
