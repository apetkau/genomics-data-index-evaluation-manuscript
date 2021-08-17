$line = 0;
while (<>) {
    chomp;
    if (($line % 4) == 0) {
        $read_number = int($line/4) + 1;
        $_ =~ s/^@(.*)-[0-9]+-[RF]/@\1-\Q$read_number\E/;
	print "$_\n";
    } else {
        print "$_\n";
    }

    $line++;
}
