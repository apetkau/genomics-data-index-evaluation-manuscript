$line = 0;
while (<>) {
    chomp;
    if (($line % 4) == 0) {
        $_ =~ s/^(@.*)_forward(.*)/\1\2/;
        $_ =~ s/^(@.*)_reverse(.*)/\1\2/;
	print "$_\n";
    } else {
        print "$_\n";
    }

    $line++;
}
