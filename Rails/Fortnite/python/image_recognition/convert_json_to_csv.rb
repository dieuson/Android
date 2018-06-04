require 'json'
require 'csv'
require 'awesome_print'
require 'date'

def post_process_slash(date)
	date = date.gsub(" ", "").gsub("201B", "2018")
	date = date.split("/")
	format_date = "#{date[0]}/#{date[1]}/#{date[2][0..3]}"

	datetime = date[2][4..date[2].size]
	hour = datetime[0...2]
	minutes = datetime[(datetime.size - 2)...datetime.size]
	new_datetime = "#{hour}:#{minutes}"

	new_date = "#{format_date} #{new_datetime}"
	return new_date
end

def post_process_dash(date)
	date = date.gsub("—", "-")
	date = date.split("-")
	format_date = "#{date[0]}-#{date[1]}-#{date[2][0..1]}"
	datetime = date[2][2..date[2].size]
	hour = datetime[0...2]
	minutes = datetime[(datetime.size - 2)...datetime.size]
	new_datetime = "#{hour}:#{minutes}".gsub("-", "")
	new_date = "#{format_date} #{new_datetime}"
	return new_date
end


def post_processing_date(date)
	date = date.gsub(" ", "").gsub(";", ":")
	new_date = nil
	if (date.include?("/"))
		new_date = post_process_slash(date)
	elsif(date.include?("-"))
		new_date = post_process_dash(date)
	end
	new_date
end

def post_processing_rank(rank)
	new_rank = rank.gsub("O", "0").gsub(" ", "")
	new_rank
end

def post_processing_eliminations(eliminations)
	new_eliminations = eliminations.gsub("O", "0").gsub("D", "0").gsub(" ", "").gsub(":", "8")
	new_eliminations
end

def post_processing_duration(duration)

	duration = duration.gsub(" ", "")
	if (duration.size == 4)
		duration = "0#{duration}"
	end
	hour = duration[0...2]
	minutes = duration[(duration.size - 2)...duration.size]
	new_duration = "#{hour}:#{minutes}"
	return new_duration
end


def compare_algo_results()
	filename = "algo analyse screenshots - sample.csv"
	results = CSV.read(filename, {:headers => true, :header_converters => :symbol})

	name_valid = 0
	name_invalid = 0

	date_valid = 0
	date_invalid = 0

	duration_valid = 0
	duration_invalid = 0

	rank_valid = 0
	rank_invalid = 0

	eliminations_valid = 0
	eliminations_invalid = 0


	results.each do |result|
		if (result[:name] != result[:expected_name])
			name_invalid += 1
		else
			name_valid += 1
		end

		tmp = post_processing_date(result[:date])
		if (tmp)
			result[:date] = tmp
		end

		if (result[:date] != result[:expected_date])
			date_invalid += 1
		else
			date_valid += 1
		end

		tmp = post_processing_duration(result[:duration])
		prev_duration = result[:duration]
		if (tmp)
			result[:duration] = tmp
		end
		if (result[:duration] != result[:expected_duration])
			# puts "Prev: #{prev_duration}, Result: #{result[:duration]}, Expected: #{result[:expected_duration]}"
			duration_invalid += 1
		else
			duration_valid += 1
		end


		tmp = post_processing_rank(result[:rank])
		if (tmp)
			result[:rank] = tmp
		end
		if (result[:rank] != result[:expected_rank])
			rank_invalid += 1
		else
			rank_valid += 1
		end

		tmp = post_processing_eliminations(result[:eliminations])
		if (tmp)
			result[:eliminations] = tmp
		end
		if (result[:eliminations] != result[:expected_eliminations])
			eliminations_invalid += 1
		else
			eliminations_valid += 1
		end
	end

	name_ratio = ((name_valid / (name_invalid + name_valid)).to_f * 100).round(2)
	date_ratio = ((date_valid / (date_invalid + date_valid.to_f)).to_f * 100).round(2)
	duration_ratio = ((duration_valid / (duration_invalid + duration_valid.to_f)).to_f * 100).round(2)
	rank_ratio = ((rank_valid / (rank_invalid + rank_valid.to_f)).to_f * 100).round(2)
	eliminations_ratio = ((eliminations_valid / (eliminations_invalid + eliminations_valid.to_f)).to_f * 100).round(2)

	puts "Name: #{name_ratio}"
	puts "Date: #{date_ratio}"
	puts "Duration: #{duration_ratio}"
	puts "Rank: #{rank_ratio}"
	puts "Eliminations: #{eliminations_ratio}"



end

def convert_json_inscrits_to_csv()
	all_csv_lines = []
	# directory = Tournament.tournament_directory
	# filename = "#{directory}/inscriptions/inscrits.json"
	filename = 'all_screenshots_data.json'
	header = ["path", "name", "date", "duration", "rank", "eliminations", "expected_name", "expected_date", "expected_duration", "expected_rank", "expected_eliminations"]
	json_data = JSON.parse(File.read(filename))
	json_data.each do |file_data|
		# ap file_data
		# result = file_data["data"].map{|info|[file_data["name"], info]}
		# puts result
		csv_lines = []
		file_data["data"].each do |data|
			csv_line = []
			csv_line = [file_data["path"].split("/").last]
			csv_line.concat([data["name"], data["date"], data["duration"], data["rank"], data["eliminations"]])
			csv_line.concat([data["name"], data["date"], data["duration"], data["rank"], data["eliminations"]])
			next if data.values().include?("DATE")
			if (data.values().count == 5)
				csv_lines.push(csv_line)
			end
			# csv_line.concat(data.values())
			# csv_line.concat(data.values())
		end
		all_csv_lines.concat(csv_lines)
		# ap all_csv_lines
		# ap file_data["data"].map{|test| test.keys()}
		# break
		# csv_line.concat(file_data["members"])
		# csv_line.concat([file_data["sender"]])
		# data.push(csv_line)
		puts "\n\n"
	end

	all_csv_lines = all_csv_lines.sort_by{|line| line[0].to_s.upcase}
	all_csv_lines.unshift(header)
	csv_string = CSV.generate do |csv|
		all_csv_lines.each do |row|
			csv << row
		end
	end
	filename = "sample.csv"
	ap all_csv_lines
	File.write(filename, csv_string)
end

# convert_json_inscrits_to_csv
compare_algo_results()

