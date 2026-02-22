#!/usr/bin/env ruby



file_in = ARGV[0]
file_one = ARGV[1]
file_two = ARGV[2]


File.open(file_in) do |fin|
  fone = File.open(file_one, 'w')
  ftwo = File.open(file_two, 'w')
  while not fin.eof?
    byte_one = fin.read(1)
    byte_two = fin.read(1)
    fone.write(byte_one)
    ftwo.write(byte_two)
  end
end
