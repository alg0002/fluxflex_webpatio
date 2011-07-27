#!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� [ WebPatio ]
#�� admin.cgi - 2007/05/06
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

# �O���t�@�C����荞��
require '../scripts/init.cgi';
require $jcode;

&parse_form;
if ($in{'pass'} eq "") { &enter; }
elsif ($in{'pass'} ne $pass) { &error("�F�؃G���["); }
if ($in{'logfile'} || $in{'bakfile'}) { &file_mente; }
elsif ($in{'filesize'}) { &filesize; }
elsif ($in{'member'} && $authkey) { &member_mente; }
&menu_disp;

#-------------------------------------------------
#  ���O�����e
#-------------------------------------------------
sub file_mente {
	local($subject,$log,$top,$itop,$sub,$res,$nam,$em,$com,$da,$ho,$pw,$re,
		$sb,$na2,$key,$last_nam,$last_dat,$del,@new,@new2,@sort,@file,@del,@top);

	# ���j���[����̏���
	if ($in{'job'} eq "menu") {
		foreach ( keys(%in) ) {
			if (/^past(\d+)/) {
				$in{'past'} = $1;
				last;
			}
		}
	}

	# �����`�F�b�N
	$in{'no'} =~ s/[^0-9\0]//g;

	# index��`
	local($mylog);
	if ($in{'bakfile'}) {
		$log = $pastfile;
		$subject = "�ߋ����O";
		$mylog = "bakfile";
	} else {
		$log = $nowfile;
		$subject = "���s���O";
		$mylog = "logfile";
	}

	# �X���b�h�ꊇ�폜
	if ($in{'action'} eq "del" && $in{'no'} ne "") {

		# �폜���
		local(@del) = split(/\0/, $in{'no'});

		# index���폜��񒊏o
		local($top, @new);
		open(DAT,"+< $log") || &error("Open Error: $log");
		eval "flock(DAT, 2);";
		$top = <DAT> if (!$in{'past'});
		while(<DAT>) {
			$flg = 0;
			local($no) = split(/<>/);
			foreach $del (@del) {
				if ($del == $no) {

					# ���O�W�J
					open(DB,"$logdir/$del.cgi");
					while( $db = <DB> ) {
						local($no,$sub,$nam,$eml,$com,$dat,$ho,$pw,$url,$mvw,$myid,$tim,$upl{1},$upl{2},$upl{3}) = split(/<>/, $db);

						# �摜�폜
						foreach $i (1 .. 3) {
							next if (!$upl{$i});

							local($ex) = split(/,/, $upl{$i});
							if (-e "$upldir/$tim-$i$ex") {
								unlink("$upldir/$tim-$i$ex");
							}
						}
					}
					close(DB);

					# �X���b�h�폜
					unlink("$logdir/$del.cgi");
					unlink("$logdir/$del.dat");
					$flg = 1;
					last;
				}
			}
			if (!$flg) { push(@new,$_); }
		}

		# index�X�V
		unshift(@new,$top);
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

	# �X���b�h�̃��b�N�J��
	} elsif ($in{'action'} eq "lock" && $in{'no'} ne "" && !$in{'past'}) {

		# ���b�N���
		local(@lock) = split(/\0/, $in{'no'});

		# �X���b�h�w�b�_���X�V
		foreach (@lock) {

			local($top,@file);
			open(DAT,"+< $logdir/$_.cgi") || &error("Open Error: $_.cgi");
			eval "flock(DAT, 2);";
			@file = <DAT>;

			$top = shift(@file);

			# �擪�L�������A�L�[�J��
			local($num,$sub,$res,$key) = split(/<>/, $top);

			# 0=���b�N 1=�W�� 2=�Ǘ��p
			if ($key eq '0') { $key = 1; } else { $key = 0; }

			# �X���b�h�X�V
			unshift(@file,"$num<>$sub<>$res<>$key<>\n");
			seek(DAT, 0, 0);
			print DAT @file;
			truncate(DAT, tell(DAT));
			close(DAT);
		}

		# index�ǂݍ���
		local($top,@new);
		open(DAT,"+< $log") || &error("Open Error: $log");
		eval "flock(DAT, 2);";
		$top = <DAT>;
		while(<DAT>) {
			s/\n//;
			local($no,$sub,$res,$nam,$da,$na2,$key,$upl) = split(/<>/);

			foreach $lock (@lock) {
				# 0=���b�N 1=�W�� 2=�Ǘ��p
				if ($lock == $no) {
					if ($key eq '0') { $key = 1; } else { $key = 0; }
					$_ = "$no<>$sub<>$res<>$nam<>$da<>$na2<>$key<>$upl<>";
				}
			}
			push(@new,"$_\n");
		}

		# index�X�V
		unshift(@new,$top);
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

	# �X���b�h�̊Ǘ��҃R�����g���[�h
	} elsif ($in{'action'} eq "lock2" && $in{'no'} ne "" && !$in{'past'}) {

		# ���b�N���
		local(@lock) = split(/\0/, $in{'no'});

		# �X���b�h�w�b�_���X�V
		foreach (@lock) {

			local($top, @file);
			open(DAT,"+< $logdir/$_.cgi") || &error("Open Error: $_.cgi");
			eval "flock(DAT, 2);";
			@file = <DAT>;

			$top = shift(@file);

			# �擪�L�������A�L�[�J��
			local($num,$sub,$res,$key) = split(/<>/, $top);

			# 0=���b�N 1=�W�� 2=�Ǘ��p
			if ($key < 2) { $key = 2; } else { $key = 1; }

			# �X���b�h�X�V
			unshift(@file,"$num<>$sub<>$res<>$key<>\n");
			seek(DAT, 0, 0);
			print DAT @file;
			truncate(DAT, tell(DAT));
			close(DAT);
		}

		# index�ǂݍ���
		local($top, $flg, @new, @top1, @top2);
		open(DAT,"+< $log") || &error("Open Error: $log");
		eval "flock(DAT, 2);";
		$top = <DAT>;
		while(<DAT>) {
			$flg = 0;
			s/\n//;
			local($no,$sub,$res,$nam,$da,$na2,$key,$upl) = split(/<>/);

			foreach $lock (@lock) {
				if ($lock == $no) {
					# 0=���b�N 1=�W�� 2=�Ǘ��p
					if ($key == 2) {
						$key = 1;
						$_ = "$no<>$sub<>$res<>$nam<>$da<>$na2<>$key<>$upl<>";
					} else {
						$key = 2;
						push(@top1,"$no<>$sub<>$res<>$nam<>$da<>$na2<>$key<>$upl<>\n");
						$flg = 1;
					}
					last;
				}
			}
			if (!$flg) {
				if ($key == 2) {
					push(@top2,"$_\n");
				} else {
					push(@new,"$_\n");
				}
			}
		}

		# index�X�V
		unshift(@new,@top2) if (@top2 > 0);
		unshift(@new,@top1) if (@top1 > 0);
		unshift(@new,$top);
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

	# �X���b�h�����X�L���{��
	} elsif ($in{'action'} eq "view" && $in{'no'} ne "") {

		# ���X�L���ʍ폜
		if ($in{'job'} eq "del" && $in{'no2'} ne "") {

			local($top,$num,$sub2,$res,$key,$flg,@del,@new);

			if ($in{'no2'} =~ /\b0\b/) {
				&error("�e�L���̍폜�͂ł��܂���");
			}

			# �폜����z��
			@del = split(/\0/, $in{'no2'});

			# �X���b�h�����폜�L���𒊏o
			local($top, @new);
			open(DAT,"+< $logdir/$in{'no'}.cgi");
			eval "flock(DAT, 2);";
			$top = <DAT>;
			local($num,$sub2,$res,$key) = split(/<>/, $top);
			while(<DAT>) {
				$flg = 0;
				local($no,$sub,$nam,$em,$com,$da,$ho,$pw,$url,$mvw,$myid,$tim,$upl{1},$upl{2},$upl{3}) = split(/<>/);
				foreach $del (@del) {
					if ($no == $del) {
						$flg = 1;

						# �摜�폜
						foreach $i (1 .. 3) {
							next if (!$upl{$i});

							local($ex) = split(/,/, $upl{$i});
							if (-e "$upldir/$tim-$i$ex") {
								unlink("$upldir/$tim-$i$ex");
							}
						}

						last;
					}
				}
				if (!$flg) {
					push(@new,$_);

					# �ŏI���e�Җ��Ǝ��Ԃ��o���Ă���
					$last_nam = $nam;
					$last_dat = $da;
				}
			}

			# ���X���𒲐�
			$res -= @del;
			$top = "$num<>$sub2<>$res<>$key<>\n";

			# �X���b�h�X�V
			unshift(@new,$top);
			seek(DAT, 0, 0);
			print DAT @new;
			truncate(DAT, tell(DAT));
			close(DAT);

			# index���e�����ւ�
			@new2 = (); @sort = (); @top = ();
			open(DAT,"+< $log");
			eval "flock(DAT, 2);";
			$top2 = <DAT> if ($in{'past'} == 0);
			while(<DAT>) {
				s/\n//;
				local($no,$sb,$re,$na,$da,$na2,$key,$upl) = split(/<>/);

				if ($key == 2) {
					push(@top,"$_\n");
					next;
				}
				if ($in{'no'} == $no) {
					# ���X���ƍŏI���e�Җ�������
					$na2 = $last_nam;
					$da  = $last_dat;
					$_ = "$no<>$sb<>$res<>$na<>$da<>$na2<>$key<>$upl<>";
				}
				push(@new2,"$_\n");

				# �\�[�g�p�z��
				$da =~ s/\D//g;
				push(@sort,$da);
			}

			# ���e���Ƀ\�[�g
			@new2 = @new2[sort {$sort[$b] <=> $sort[$a]} 0 .. $#sort];

			# index�X�V
			unshift(@new2,@top) if (@top > 0);
			unshift(@new2,$top2) if ($in{'past'} == 0);
			seek(DAT, 0, 0);
			print DAT @new2;
			truncate(DAT, tell(DAT));
			close(DAT);

		# ���X�L���ʏC��
		} elsif ($in{'job'} eq "edit" && $in{'no2'} ne "") {

			# �����I���̏ꍇ�͐擪�̂�
			($in{'no2'}) = split(/\0/, $in{'no2'});

			require $editlog;
			&edit_log("admin");
		}

		# �X���b�h���ʉ{��
		&header;
		print "<div align=\"right\">\n";
		print "<form action=\"$admincgi\" method=\"post\">\n";
		print "<input type=\"hidden\" name=\"pass\" value=\"$in{'pass'}\">\n";
		print "<input type=\"hidden\" name=\"mode\" value=\"admin\">\n";
		print "<input type=\"hidden\" name=\"$mylog\" value=\"1\">\n";
		print "<input type=\"submit\" value=\"&lt;&lt; �߂�\"></form></div>\n";
		print "<form action=\"$admincgi\" method=\"post\">\n";
		print "<input type=\"hidden\" name=\"pass\" value=\"$in{'pass'}\">\n";
		print "<input type=\"hidden\" name=\"mode\" value=\"admin\">\n";
		print "<input type=\"hidden\" name=\"$mylog\" value=\"1\">\n";
		print "<input type=\"hidden\" name=\"no\" value=\"$in{'no'}\">\n";
		print "<input type=\"hidden\" name=\"action\" value=\"view\">\n";

		open(IN,"$logdir/$in{'no'}.cgi");
		$top = <IN>;
		($num,$sub,$res) = split(/<>/, $top);

		print "�X���b�h�� �F <b>$sub</b> [ $subject ]<hr>\n";
		print "<li>�C�����͍폜��I�����ċL�����`�F�b�N���܂��B<br>\n";
		print "<li>�e�L���̍폜�͂ł��܂���B<br><br>\n";
		print "���� �F <select name=\"job\">\n";
		print "<option value=\"edit\" selected>�C��\n";
		print "<option value=\"del\">�폜</select>\n";
		print "<input type=\"submit\" value=\"���M����\">\n";
		print "<dl>\n";

		while (<IN>) {
			local($no,$sub,$nam,$em,$com,$da,$ho,$pw,$url,$mvw,$myid) = split(/<>/);

			if ($em) { $nam="<a href=\"mailto:$em\">$nam</a>"; }

			print "<dt><input type=\"checkbox\" name=\"no2\" value=\"$no\"> ";
			print "[<b>$no</b>] <b>$nam</b> - $da ";
			print "�y<font color=\"$al\">$ho</font>�z\n";

			if ($authkey) { print "ID:$myid\n"; }

			print "<dd>$com\n";
		}
		close(IN);

		print "</dl></form>\n</body></html>\n";
		exit;
	}

	&header;
	print <<"EOM";
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value="&lt; �Ǘ�TOP">
</form>
<h3 style="font-size:16px">�Ǘ����[�h [ $subject ]</h3>
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="$mylog" value="1">
�X���b�h���� <select name="action">
<option value="view">�ʃ����e
<option value="del">�X���폜
EOM

	if ($in{'past'} == 0) {
		print "<option value=\"lock\">���b�N�J��\n";
		print "<option value=\"lock2\">�Ǘ���\n";
	}

	print <<EOM;
</select>
<input type="submit" value="���M����">
<p>
<Table border="0" cellspacing="0" cellpadding="0" width="400">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="4" width="100%">
<tr bgcolor="$col1">
  <td bgcolor="$col3" align="center" nowrap>�I��</td>
  <td bgcolor="$col3" width="100%">&nbsp; �X���b�h</td>
  <td bgcolor="$col3" align="center" nowrap>���X��</td>
</tr>
EOM

	# �X���b�h�ꗗ
	open(IN,"$log") || &error("Open Error: $log");
	$top = <IN> if (!$in{'bakfile'});
	while (<IN>) {
		local($no,$sub,$res,$nam,$da,$na2,$key) = split(/<>/);

		print "<tr bgcolor=\"$col2\"><th bgcolor=\"$col2\">";
		print "<input type=checkbox name=\"no\" value=\"$no\"></th>";
		print "<td bgcolor=\"$col2\">";

		if ($key eq '0') {
			print "[<font color=\"$al\">���b�N��</font>] ";
		} elsif ($key == 2) {
			print "[<font color=\"$al\">�Ǘ��R�����g</font>] ";
		}

		print "<b>$sub</b></td>";
		print "<td bgcolor=\"$col2\" align=\"center\">$res</td></tr>\n";
	}
	close(IN);

	print <<EOM;
</table>
</Td></Tr></Table>
</form>
</body>
</html>
EOM

	exit;
}

#-------------------------------------------------
#  �t�@�C���T�C�Y
#-------------------------------------------------
sub filesize {
	local($top,$tmp,$num,$all,$all2,$size1,$size2,$size3,$size4,$file,$file1,$file2);

	# ���s���O
	$size1 = 0;
	$file1 = 0;
	open(IN,"$nowfile") || &error("Open Error: $nowfile");
	$top = <IN>;
	while (<IN>) {
		($num) = split(/<>/);
		$tmp = -s "$logdir/$num.cgi";
		$size1 += $tmp;
		$file1++;

		$now{$num} = 1;
	}
	close(IN);

	# �ߋ����O
	$size2 = 0;
	$file2 = 0;
	open(IN,"$pastfile") || &error("Open Error: $pastfile");
	while (<IN>) {
		($num) = split(/<>/);
		$tmp = -s "$logdir/$num.cgi";
		$size2 += $tmp;
		$file2++;

		$pst{$num} = 1;
	}
	close(IN);

	# �摜
	opendir(DIR,"$upldir");
	local(@dir) = readdir(DIR);
	closedir(DIR);

	local($img) = 0;
	foreach (@dir) {
		next unless (/^[\d\-]+\.(jpg|gif|png)$/);

		$img += -s "$upldir/$_";
	}

	$size1 = int ($size1 / 1024 + 0.5);
	$size2 = int ($size2 / 1024 + 0.5);
	$img   = int ($img / 1024 + 0.5);
	$all = $size1 + $size2;
	$file = $file1 + $file2;

	&header;
	print <<"EOM";
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value="&lt; �Ǘ�TOP">
</form>
<h3 style="font-size:16px">���O�e�ʎZ�o</h3>
<ul>
<li>�ȉ��͋L�^�t�@�C���̗e�ʁi�T�C�Y�j�ŁA�����_�ȉ��͎l�̌ܓ����܂��B
<li>���ޗ��̃t�H�[�����N���b�N����Ɗe�Ǘ���ʂɈړ����܂��B
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<p>
<Table border="0" cellspacing="0" cellpadding="0" width="280">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col1">
  <td bgcolor="$col3" rowspan="2" align="center">����</td>
  <td bgcolor="$col3" rowspan="2" width="70" align="center">�t�@�C����</td>
  <td bgcolor="$col3" colspan="2" align="center">�T�C�Y</td>
</tr>
<tr bgcolor="$col1">
  <td bgcolor="$col3" align="center" width="50">���O</td>
  <td bgcolor="$col3" align="center" width="50">�摜</td>
</tr>
<tr>
  <th bgcolor="$col2">
   <input type="submit" name="logfile" value="���s���O"></th>
  <td align="right" bgcolor="$col2">$file1</td>
  <td align="right" bgcolor="$col2">$size1 KB</td>
  <td align="right" bgcolor="$col2" rowspan="2">$img KB</td>
</tr>
<tr bgcolor="$col2">
  <th bgcolor="$col2">
   <input type="submit" name="bakfile" value="�ߋ����O"></th>
  </th>
  <td align="right" bgcolor="$col2">$file2</td>
  <td align="right" bgcolor="$col2">$size2 KB</td>
</tr>
<tr bgcolor="$col2">
  <th bgcolor="$col2">���v</th>
  <td align="right" bgcolor="$col2">$file</td>
  <td align="right" bgcolor="$col2">$all KB</td>
  <td align="right" bgcolor="$col2">$img KB</td>
</tr>
</table>
</Td></Tr></Table>
</form>
</ul>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  ����Ǘ�
#-------------------------------------------------
sub member_mente {
	# �V�K�t�H�[��
	if ($in{'job'} eq "new") {

		&member_form();

	# �V�K���s
	} elsif ($in{'job'} eq "new2") {

		local($err);
		if (!$in{'name'}) { $err .= "���O�������͂ł�<br>\n"; }
		if ($in{'myid'} =~ /\W/) { $err .= "ID�͉p�����݂̂ł�<br>\n"; }
		if (length($in{'myid'}) < 4 || length($in{'myid'}) > 8) {
			$err .= "ID�͉p������4�`8�����ł�<br>\n";
		}
		if ($in{'mypw'} =~ /\W/) { $err .= "�p�X���[�h�͉p�����݂̂ł�<br>\n"; }
		if (length($in{'mypw'}) < 4 || length($in{'mypw'}) > 8) {
			$err .= "�p�X���[�h�͉p������4�`8�����ł�<br>\n";
		}
		if (!$in{'rank'}) { $err .= "���������I���ł�<br>\n"; }
		if ($err) { &error($err); }

		local($flg,$crypt,$id,$pw,$rank,$nam,@data);

		# ID�`�F�b�N
		$flg = 0;
		open(DAT,"+< $memfile") || &error("Open Error: $memfile");
		while(<DAT>) {
			local($id,$pw,$rank,$nam) = split(/<>/);

			if ($in{'myid'} eq $id) { $flg = 1; last; }
			push(@data,$_);
		}

		if ($flg) { &error("����ID�͊��ɓo�^�ςł�"); }

		# �p�X�Í���
		$crypt = &encrypt($in{'mypw'});

		# �X�V
		seek(DAT, 0, 0);
		print DAT "$in{'myid'}<>$crypt<>$in{'rank'}<>$in{'name'}<>\n";
		print DAT @data;
		truncate(DAT, tell(DAT));
		close(DAT);

	# �C���t�H�[��
	} elsif ($in{'job'} eq "edit" && $in{'myid'}) {

		if ($in{'myid'} =~ /\0/) { &error("�C���I���͂P�݂̂ł�"); }

		local($flg,$id,$pw,$rank,$nam);

		$flg = 0;
		open(IN,"$memfile") || &error("Open Error: $memfile");
		while (<IN>) {
			($id,$pw,$rank,$nam) = split(/<>/);

			if ($in{'myid'} eq $id) { $flg = 1; last; }
		}
		close(IN);

		&member_form($id,$pw,$rank,$nam);

	# �C�����s
	} elsif ($in{'job'} eq "edit2") {

		local($err,$crypt);
		if (!$in{'name'}) { $err .= "���O�������͂ł�<br>\n"; }
		if ($in{'myid'} =~ /\W/) { $err .= "ID�͉p�����݂̂ł�<br>\n"; }
		if (length($in{'myid'}) < 4 || length($in{'myid'}) > 8) {
			$err .= "ID�͉p������4�`8�����ł�<br>\n";
		}
		if ($in{'chg'}) {
			if ($in{'mypw'} =~ /\W/) { $err .= "�p�X���[�h�͉p�����݂̂ł�<br>\n"; }
			if (length($in{'mypw'}) < 4 || length($in{'mypw'}) > 8) {
				$err .= "�p�X���[�h�͉p������4�`8�����ł�<br>\n";
			}

			# �p�X�Í���
			$crypt = &encrypt($in{'mypw'});

		} elsif (!$in{'chg'} && $in{'mypw'} ne "") {
			$err .= "�p�X���[�h�̋����ύX�̓`�F�b�N�{�b�N�X�ɑI�����Ă�������<br>\n";
		}
		if (!$in{'rank'}) { $err .= "���������I���ł�<br>\n"; }
		if ($err) { &error($err); }

		local($flg,$id,$pw,$rank,$nam,@data);

		open(DAT,"+< $memfile") || &error("Open Error: $memfile");
		while(<DAT>) {
			local($id,$pw,$rank,$nam) = split(/<>/);

			if ($in{'myid'} eq $id) {
				if ($crypt) { $pw = $crypt; }
				$_ = "$id<>$pw<>$in{'rank'}<>$in{'name'}<>\n";
			}
			push(@data,$_);
		}

		# �X�V
		seek(DAT, 0, 0);
		print DAT @data;
		truncate(DAT, tell(DAT));
		close(DAT);

	# �폜
	} elsif ($in{'job'} eq "dele" && $in{'myid'}) {

		local($flg,@data,@del);

		# �폜���
		@del = split(/\0/, $in{'myid'});

		open(DAT,"+< $memfile") || &error("Open Error: $memfile");
		while(<DAT>) {
			local($id,$pw,$rank,$nam) = split(/<>/);

			$flg = 0;
			foreach $del (@del) {
				if ($del eq $id) { $flg = 1; last; }
			}
			if (!$flg) { push(@data,$_); }
		}

		# �X�V
		seek(DAT, 0, 0);
		print DAT @data;
		truncate(DAT, tell(DAT));
		close(DAT);
	}

	&header;
	print <<"EOM";
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value="&lt; �Ǘ�TOP">
</form>
<h3 style="font-size:16px">����Ǘ�</h3>
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="member" value="1">
<input type="hidden" name="past" value="3">
���� :
<select name="job">
<option value="new">�V�K
<option value="edit">�C��
<option value="dele">�폜
</select>
<input type="submit" value="���M����">
<p>
<Table border="0" cellspacing="0" cellpadding="0" width="280">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="3" width="100%">
<tr bgcolor="$col1">
  <td bgcolor="$col3" align="center" nowrap width="30">�I��</td>
  <td bgcolor="$col3" align="center" nowrap>ID</td>
  <td bgcolor="$col3" align="center" nowrap>���O</td>
  <td bgcolor="$col3" align="center" nowrap>�����N</td>
</tr>
EOM

	open(IN,"$memfile") || &error("Open Error: $memfile");
	while (<IN>) {
		($id,$pw,$rank,$nam) = split(/<>/);

		print "<tr bgcolor=\"$col2\"><th bgcolor=\"$col2\">";
		print "<input type=\"checkbox\" name=\"myid\" value=\"$id\"></th>";
		print "<td bgcolor=\"$col2\" nowrap>$id</td>";
		print "<td bgcolor=\"$col2\">$nam</td>";
		print "<td bgcolor=\"$col2\" align=\"center\">$rank</td>";
	}
	close(IN);

	print <<EOM;
</table>
</Td></Tr></Table>
</form>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  ����t�H�[��
#-------------------------------------------------
sub member_form {
	local($id,$pw,$rank,$nam) = @_;
	local($job) = $in{'job'} . '2';

	&header();
	print <<EOM;
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="member" value="1">
<input type="submit" value="&lt; �O���">
</form>
<h3 style="font-size:16px">�o�^�t�H�[��</h3>
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="member" value="1">
<input type="hidden" name="job" value="$job">
<Table border="0" cellspacing="0" cellpadding="0" width="350">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col1">
  <td bgcolor="$col2" align="center" nowrap>���O</td>
  <td bgcolor="$col2"><input type="text" name="name" size="25" value="$nam"></td>
</tr>
<tr bgcolor="$col1">
  <td bgcolor="$col2" align="center" nowrap>���O�C��ID</td>
  <td bgcolor="$col2">
EOM

	if ($in{'myid'}) {
		print $in{'myid'};
	} else {
		print "<input type=\"text\" name=\"myid\" size=\"10\" value=\"$id\">\n";
		print "�i�p������4�`8�����j\n";
	}

	print <<EOM;
  </td>
</tr>
<tr bgcolor="$col1">
  <td bgcolor="$col2" align="center" nowrap>�p�X���[�h</td>
  <td bgcolor="$col2">
	<input type="password" name="mypw" size="10"> �i�p������4�`8�����j
EOM

	if ($in{'myid'}) {
		print "<br><input type=\"checkbox\" name=\"chg\" value=\"1\">\n";
		print "�p�X���[�h�������ύX����ꍇ�Ƀ`�F�b�N\n";
		print "<input type=\"hidden\" name=\"myid\" value=\"$in{'myid'}\">\n";
	}

	print <<EOM;
  </td>
</tr>
<tr bgcolor="$col1">
  <td bgcolor="$col2" align="center" nowrap>����</td>
  <td bgcolor="$col2">
EOM

	local(%rank) = (1,"�{���̂�", 2,"�{��&amp;����OK");
	foreach (1,2) {
		if ($rank == $_) {
			print "<input type=radio name=rank value=\"$_\" checked>���x��$_ ($rank{$_})<br>\n";
		} else {
			print "<input type=radio name=rank value=\"$_\">���x��$_ ($rank{$_})<br>\n";
		}
	}

	print <<EOM;
  </td>
</tr>
</table>
</Td></Tr></Table>
<p>
<input type="submit" value="���M����">
</form>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  ���j���[���
#-------------------------------------------------
sub menu_disp {
	# �Z�b�V�����f�B���N�g���|��
	if ($authkey && $in{'login'}) {
		&ses_clean;
	}

	&header;
	print <<EOM;
<form action="$bbscgi">
<input type="submit" value="&lt; �f����">
</form>
<div align="center">
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="job" value="menu">
�������e��I�����Ă��������B
<p>
<Table border="0" cellspacing="0" cellpadding="0" width="320">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col1">
  <td bgcolor="$col3" align="center">
	�I��
  </td>
  <td bgcolor="$col3" width="100%">
	&nbsp; �������e
  </td>
</tr>
<tr bgcolor="$col2">
  <td bgcolor="$col2" align="center">
	<input type="submit" name="logfile" value="�I��">
  </td>
  <td bgcolor="$col2" width="100%">
	&nbsp; ���s���O�E�����e�i���X
  </td>
</tr>
<tr bgcolor="$col2">
  <td bgcolor="$col2" align="center">
	<input type="submit" name="bakfile" value="�I��">
  </td>
  <td bgcolor="$col2" width="100%">
	&nbsp; �ߋ����O�E�����e�i���X
  </td>
</tr>
EOM

	if ($authkey) {
		print "<tr bgcolor=\"$col2\"><td bgcolor=\"$col2\" align=\"center\">\n";
		print "<input type=\"submit\" name=\"member\" value=\"�I��\"></td>";
		print "<td bgcolor=\"$col2\" width=\"100%\">&nbsp; ����F�؂̊Ǘ�</td></tr>\n";
	}

	print <<EOM;
<tr bgcolor="$col2">
  <td bgcolor="$col2" align="center">
	<input type="submit" name="filesize" value="�I��">
  </td>
  <td bgcolor="$col2" width="100%">
	&nbsp; �t�@�C���e�ʂ̉{��
  </td>
</tr>
</table>
</Td></Tr></Table>
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �������
#-------------------------------------------------
sub enter {
	&header;
	print <<EOM;
<blockquote>
<table border="0" cellspacing="0" cellpadding="26" width="400">
<tr><td align="center">
	<fieldset>
	<legend>
	���Ǘ��p�X���[�h����
	</legend>
	<form action="$admincgi" method="post">
	<input type="hidden" name="login" value="1">
	<input type="password" name="pass" size="16">
	<input type="submit" value=" �F�� "></form>
	</fieldset>
</td></tr>
</table>
</blockquote>
<script language="javascript">
<!--
self.document.forms[0].pass.focus();
//-->
</script>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �Z�V�����f�B���N�g���|��
#-------------------------------------------------
sub ses_clean {
	local($mtime,@dir);

	opendir(DIR,"$sesdir");
	@dir = readdir(DIR);
	closedir(DIR);

	foreach (@dir) {
		next unless (/^\w+\.cgi$/);

		$mtime = (stat("$sesdir/$_"))[9];
		if (time - $mtime > $authtime*60*2) {
			unlink("$sesdir/$_");
		}
	}
}

