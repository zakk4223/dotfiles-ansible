#!/usr/bin/env ruby



file_one = ARGV[0]
file_two = ARGV[1]
out_file = ARGV[2]


File.open(out_file, 'wb') do |fout|
  File.open(file_one) do |fone|

    File.open(file_two) do |ftwo|
      while obyte = fone.read(1)
        tbyte = ftwo.read(1)
        fout.write(obyte)
        fout.write(tbyte)
      end
    end
  end
end


