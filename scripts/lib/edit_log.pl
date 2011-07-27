#��������������������������������������������������������������������
#�� [ WebPatio ]
#�� edit_log.pl - 2011/07/06
#�� Copyright (c) KentWeb
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

#-------------------------------------------------
#  �L���C��
#-------------------------------------------------
sub edit_log {
	local($myjob) = @_;

	if ($myjob eq "admin") {
		$in{'f'}  = $in{'no'};
		$in{'no'} = $in{'no2'};
	}
	local($mylog,$idxfile);
	if ($in{'bakfile'}) {
		$idxfile = $pastfile;
		$mylog = 'bakfile';
	} else {
		$idxfile = $nowfile;
		$mylog = 'logfile';
	}

	# �����`�F�b�N
	$in{'f'}  =~ s/\D//g;
	$in{'no'} =~ s/\D//g;

	# �C������
	if ($in{'job'} eq "edit2") {

		# �Ǘ��҃I�y
		if ($in{'pass'} ne "") {
			$admin_flag = 1;
			if ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

		# ���[�U�I�y
		} elsif ($in{'pwd'} ne "") {
			$admin_flag = 0;

			# �`�F�b�N
			if ($no_wd) { &no_wd; }
			if ($jp_wd) { &jp_wd; }
			if ($urlnum > 0) { &urlnum; }

		# �I�y�s��
		} else {
			&error("�s���ȃA�N�Z�X�ł�");
		}

		# ���e���e�`�F�b�N
		if ($i_com eq "") { &error("�R�����g�̓��e������܂���"); }
		if ($i_nam eq "") {
			if ($in_name) { &error("���O�͋L���K�{�ł�"); }
			else { $i_nam = '�������̃S���x�G'; }
		}
		if ($in_mail && $in{'email'} eq "") { &error("E-mail�͋L���K�{�ł�"); }
		if ($in{'email'} && $in{'email'} !~ /^[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/)
			{ &error("E-mail�̓��͓��e���s���ł�"); }
		if ($i_sub eq "")
			{ &error("�^�C�g���͋L���K�{�ł�"); }
		if ($i_sub =~ /^(\x81\x40|\s)+$/)
			{ &error("�^�C�g���͐������L�����Ă�������"); }
		if ($i_nam =~ /^(\x81\x40|\s)+$/)
			{ &error("���O�͐������L�����Ă�������"); }
		if ($i_com =~ /^(\x81\x40|\s|<br>)+$/)
			{ &error("�R�����g�͐������L�����Ă�������"); }
		if ($in{'url'} eq "http://") { $in{'url'} = ""; }
		elsif ($in{url} && $in{url} !~ /^https?:\/\/[\w-.!~*'();\/?:\@&=+\$,%#]+$/) {
			&error("URL��񂪕s���ł�");
		}

		local($top, @new);
		open(DAT,"+< $logdir/$in{'f'}.cgi") || &error("Open Error: $in{'f'}.cgi");
		eval "flock(DAT, 2);";
		$top = <DAT>;
		while(<DAT>) {
			s/\n//;
			local($no,$sub,$nam,$eml,$com,$dat,$hos,$pw,$url,$mvw,$myid,$tim,$upl1,$upl2,$upl3) = split(/<>/);

			if ($in{'no'} == $no) {

				# �p�X�`�F�b�N
				if (!$admin_flag) {
					if (!&decrypt($in{'pwd'}, $pw)) {
						&error("�p�X���[�h���Ⴂ�܂�");
					}
				}

				# �g���b�v
				unless ($i_nam =~ /��/ && $i_nam eq $nam) {
					$i_nam = &trip($i_nam);
				}

				# �Y�t�g���q
				local($ex1) = split(/,/, $upl1);
				local($ex2) = split(/,/, $upl2);
				local($ex3) = split(/,/, $upl3);

				# �摜
				if (!$in{'no'}) {

					# �Y�t�폜
					if ($in{'del1'}) {
						$upl1 = '';
						unlink("$upldir/$tim-1$ex1");
					}
					if ($in{'del2'}) {
						$upl2 = '';
						unlink("$upldir/$tim-2$ex2");
					}
					if ($in{'del3'}) {
						$upl3 = '';
						unlink("$upldir/$tim-3$ex3");
					}

					# �e�L�����Y�t�A�b�v
					if ($image_upl && ($in{'upfile1'} || $in{'upfile2'} || $in{'upfile3'})) {

						if ($tim eq "") { &error("���̋L���̓A�b�v���[�h�ł��܂���"); }

						require $upload;
						local($ex{1},$w1,$h1,$ex{2},$w2,$h2,$ex{3},$w3,$h3) = &upload($tim);
						if ($ex{1}) {
							$upl1 = "$ex{1},$w1,$h1";
							if ($ex1 && $ex1 ne $ex{1}) {
								unlink("$upldir/$tim-1$ex1");
							}
						}
						if ($ex{2}) {
							$upl2 = "$ex{2},$w2,$h2";
							if ($ex2 && $ex2 ne $ex{2}) {
								unlink("$upldir/$tim-2$ex2");
							}
						}
						if ($ex{3}) {
							$upl3 = "$ex{3},$w3,$h3";
							if ($ex3 && $ex3 ne $ex{3}) {
								unlink("$upldir/$tim-3$ex3");
							}
						}
					}
				}
				$_ = "$no<>$in{'sub'}<>$i_nam<>$in{'email'}<>$in{'comment'}<>$dat<>$host<>$pw<>$in{'url'}<>$in{'mvw'}<>$myid<>$tim<>$upl1<>$upl2<>$upl3<>";

			}
			push(@new,"$_\n");
		}

		# �w�b�_
		($num,$sub2,$res2,$key) = split(/<>/, $top);

		# �e�L���̏ꍇ�͑薼���X�V
		if (!$in{'no'}) { $sub2 = $in{'sub'}; }

		# �X�V
		unshift(@new,"$num<>$sub2<>$res2<>$key<>\n");
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

		# �ŏI���e�Җ�
		($last_nam) = (split(/<>/, $new[$#new]))[2];

		# index�W�J
		local(@data);
		open(DAT,"+< $idxfile") || &error("Open Error: $idxfile");
		eval "flock(DAT, 2);";
		$top = <DAT> if (!$in{'bakfile'});
		while(<DAT>) {
			s/\n//;
			local($no,$sub,$res,$nam,$da,$na2,$key2,$upl) = split(/<>/);

			if ($in{'f'} == $no) {

				# �e�L���C���̂Ƃ�
				if (!$in{'no'}) {

					# �e���O
					local($tim,$upl1,$upl2,$upl3) = (split(/<>/, $new[1]))[11..14];
					local($ex1) = split(/,/, $upl1);
					local($ex2) = split(/,/, $upl2);
					local($ex3) = split(/,/, $upl3);
					if ($ex1 || $ex2 || $ex3) { $upl = $tim; } else { $upl = ''; }

					if ($res2 == 0) { $na2 = $i_nam; }
					$_ = "$no<>$in{'sub'}<>$res<>$i_nam<>$da<>$na2<>$key<>$upl<>";

				# ���X�L���C���̂Ƃ�
				} else {
					$_ = "$no<>$sub<>$res<>$nam<>$da<>$last_nam<>$key<>$upl<>";
				}
			}
			push(@data,"$_\n");
		}

		# index�X�V
		unshift(@data,$top) if (!$in{'bakfile'});
		seek(DAT, 0, 0);
		print DAT @data;
		truncate(DAT, tell(DAT));
		close(DAT);

		# �������b�Z�[�W
		&header;
		print "<blockquote>\n";
		print "<b>�C�������͐���Ɋ�������܂���</b>\n";

		# �Ǘ����[�h
		if ($myjob eq "admin" || $in{'myjob'} eq "admin") {
			print "<form action=\"$admincgi\" method=\"post\">\n";
			print "<input type=\"hidden\" name=\"pass\" value=\"$in{'pass'}\">\n";
			print "<input type=\"hidden\" name=\"mode\" value=\"admin\">\n";
			print "<input type=\"hidden\" name=\"$mylog\" value=\"1\">\n";

		# ��ʃ��[�h
		} else {
			print "<form action=\"$bbscgi\">\n";
		}
		print "<input type=\"submit\" value=\"�f���֖߂�\"></form>\n";
		print "</blockquote></body></html>\n";
		exit;
	}

	# �Y�����O�`�F�b�N
	local($flg, $top);
	open(IN,"$logdir/$in{'f'}.cgi");
	$top = <IN>;
	while (<IN>) {
		s/\n//;
		($no,$sub,$nam,$eml,$com,$dat,$hos,$pw,$url,$mvw,$myid,$tim,$upl{1},$upl{2},$upl{3}) = split(/<>/);

		last if ($in{'no'} == $no);
	}
	close(IN);

	if ($myjob eq "user") {
		if ($pw eq "") {
			&error("�Y���L���̓p�X���[�h���ݒ肳��Ă��܂���");
		}
		if (!&decrypt($in{'pwd'}, $pw)) { &error("�p�X���[�h���Ⴂ�܂�"); }
	}

	if ($smile) { &header("", "js"); }
	else { &header(); }

	print <<"EOM";
<div align="center">
<Table border="0" cellspacing="0" cellpadding="0" width="95%">
<Tr bgcolor="$col1"><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col3"><td bgcolor="$col3" nowrap width="92%">
<img src="$imgurl/mente.gif" align="top">
&nbsp; <b>�L���C���t�H�[��</b></td>
<td align="right" bgcolor="$col3" nowrap>
<a href="javascript:history.back()">�O��ʂɖ߂�</a></td>
</tr></table></Td></Tr></Table>
<p>
EOM

	if ($image_upl) {
		print qq|<form action="$registcgi" method="post" name="myFORM" enctype="multipart/form-data">\n|;
	} else {
		print qq|<form action="$registcgi" method="post" name="myFORM">\n|;
	}

	print <<EOM;
<input type="hidden" name="mode" value="edit_log">
<input type="hidden" name="job" value="edit2">
<input type="hidden" name="f" value="$in{'f'}">
<input type="hidden" name="no" value="$in{'no'}">
<input type="hidden" name="myjob" value="$myjob">
<input type="hidden" name="$mylog" value="1">
<Table border="0" cellspacing="0" cellpadding="0" width="95%">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col2">
  <td bgcolor="$col2" width="80" nowrap>�薼</td>
  <td><input type="text" name="sub" size="30" value="$sub" maxlength="30"></td>
</tr>
<tr bgcolor="$col2">
  <td bgcolor="$col2" width="80" nowrap>���O</td>
  <td><input type="text" name="name" size="30" value="$nam" maxlength="20"></td>
</tr>
<tr bgcolor="$col2">
  <td bgcolor="$col2" width="80" nowrap>E-Mail</td>
  <td><input type="text" name="email" size="30" value="$eml">
	<select name="mvw">
EOM

	@mvw = ('��\��','�\��');
	foreach (0,1) {
		if ($mvw == $_) {
			print "<option value=\"$_\" selected>$mvw[$_]\n";
		} else {
			print "<option value=\"$_\">$mvw[$_]\n";
		}
	}
	if ($url eq "") { $url = "http://"; }

	print <<"EOM";
</select></td>
</tr>
<tr bgcolor="$col2">
  <td bgcolor="$col2" width="80">URL</td>
  <td bgcolor="$col2"><input type="text" name="url" size="45" value="$url"></td>
</tr>
EOM

	# �e�L���͓Y�t�t�H�[��
	if ($image_upl && !$in{'no'}) {
		print "<tr bgcolor=\"$col2\"><td bgcolor=\"$col2\" width=\"80\">�Y�t</td>";
		print "<td bgcolor=\"$col2\">\n";

		foreach $i (1 .. 3) {
			local($ex) = split(/,/, $upl{$i});
			print "<input type=\"file\" name=\"upfile$i\" size=\"45\">\n";
			if ($ex) {
				print "&nbsp;[<a href=\"$upldir/$tim-$i$ex\" target=\"_blank\">�Y�t$i</a>]\n";
				print "<input type=\"checkbox\" name=\"del$i\" value=\"1\">�Y�t�폜\n";
			}
			print "<br>\n";
		}

		print "</td></tr>\n";
	}

	print <<EOM;
<tr bgcolor="$col2">
  <td bgcolor="$col2" width="80">�R�����g</td>
  <td bgcolor="$col2">
EOM

	# �A�C�R��
	if ($smile) {
		@s1 = split(/\s+/, $smile1);
		@s2 = split(/\s+/, $smile2);
		foreach (0 .. $#s1) {
			print "<a href=\"javascript:MyFace('$s2[$_]')\">";
			print "<img src=\"$imgurl/$s1[$_]\" border=0></a>\n";
		}
		print "<br>\n";
	}

	if ($myjob eq "admin") {
		print "<input type=hidden name=pass value=\"$in{'pass'}\">\n";
	} else {
		print "<input type=hidden name=pwd value=\"$in{'pwd'}\">\n";
	}

	$com =~ s/<br>/\n/g;
	print <<"EOM";
<textarea name="comment" cols="48" rows="6" wrap="soft">$com</textarea></td></tr>
<tr bgcolor="$col2">
  <td bgcolor="$col2"><br></td>
  <td bgcolor="$col2">
    <input type="submit" value="�L�����C������"></td>
  </form></tr></table>
</Td></Tr></Table>
</form></div>
</body>
</html>
EOM
	exit;
}



1;

