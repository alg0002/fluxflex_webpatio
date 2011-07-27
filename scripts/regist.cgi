#!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� [ WebPatio ]
#�� regist.cgi - 2011/07/06
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

# �O���t�@�C����荞��
require '../scripts/init.cgi';
require $jcode;

&parse_form;
&axscheck;
if ($mode eq "regist") { &regist; }
elsif ($mode eq "del") { &delete; }
elsif ($mode eq "mente") { &mente; }
elsif ($mode eq "edit_log") {
	require $editlog;
	&edit_log;
}
&error("�s���ȏ����ł�");

#-------------------------------------------------
#  �L�����e����
#-------------------------------------------------
sub regist {
	local($sub,$key,$flg,$i,@top);

	# �����`�F�b�N
	if ($authkey && $my_rank < 2) {
		&error("���e�̌���������܂���$my_rank");
	}

	# POST����
	if ($postonly && !$postflag) { &error("�s���ȃA�N�Z�X�ł�"); }

	# �`�F�b�N
	if ($no_wd) { &no_wd; }
	if ($jp_wd) { &jp_wd; }
	if ($urlnum > 0) { &urlnum; }

	# �R�����g�������`�F�b�N
	if (length($i_com) > $max_msg*2) {
		&error("�������I�[�o�[�ł��B<br>�S�p$max_msg�����ȓ��ŋL�q���Ă�������");
	}

	# �����`�F�b�N
	$in{'res'} =~ s/\D//g;

	# ���e���e�`�F�b�N
	if ($i_com eq "") { &error("�R�����g�̓��e������܂���"); }
	if ($i_nam eq "") {
		if ($in_name) { &error("���O�͋L���K�{�ł�"); }
		else { $i_nam = '�������̃S���x�G'; }
	}
	if ($in_mail && $in{'email'} eq "") { &error("E-mail�͋L���K�{�ł�"); }
	if ($in{'email'} && $in{'email'} !~ /^[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/) {
		&error("E-mail�̓��͓��e���s���ł�");
	}
	if ($i_sub eq "") { &error("�^�C�g���͋L���K�{�ł�"); }
	if ($i_sub =~ /^(\x81\x40|\s)+$/) { &error("�^�C�g���͐������L�����Ă�������"); }
	if ($i_nam =~ /^(\x81\x40|\s)+$/) { &error("���O�͐������L�����Ă�������"); }
	if ($i_com =~ /^(\x81\x40|\s|<br>)+$/) { &error("�R�����g�͐������L�����Ă�������"); }
	if ($in_pwd && $in{'pwd'} eq "") { &error("�p�X���[�h�͓��͕K�{�ł�"); }
	if (length($in{'pwd'}) > 8) { &error("�p�X���[�h��8�����ȓ��ɂ��ĉ�����"); }
	if ($in{'url'} eq "http://") { $in{'url'} = ""; }
	elsif ($in{url} && $in{url} !~ /^https?:\/\/[\w-.!~*'();\/?:\@&=+\$,%#]+$/) {
		&error("URL��񂪕s���ł�");
	}

	# ���e�L�[�`�F�b�N
	if ($regist_key) {
		require $regkeypl;

		if ($in{'regikey'} !~ /^\d{4}$/) {
			&error("���e�L�[�����͕s���ł��B<p>���e�t�H�[���ɖ߂��čēǍ��݌�A�w��̐�������͂��Ă�������");
		}

		# ���e�L�[�`�F�b�N
		# -1 : �L�[�s��v
		#  0 : �������ԃI�[�o�[
		#  1 : �L�[��v
		local($chk) = &registkey_chk($in{'regikey'}, $in{'str_crypt'});
		if ($chk == 0) {
			&error("���e�L�[���������Ԃ𒴉߂��܂����B<p>���e�t�H�[���ɖ߂��čēǍ��݌�A�w��̐������ē��͂��Ă�������");
		} elsif ($chk == -1) {
			&error("���e�L�[���s���ł��B<p>���e�t�H�[���ɖ߂��čēǍ��݌�A�w��̐�������͂��Ă�������");
		}
	}

	# �g���b�v
	$i_nam2 = &trip($i_nam);

	# �p�X���[�h�Í���
	my $pwd;
	if ($in{'pwd'} ne "") { $pwd = &encrypt($in{'pwd'}); }

	# �V�K���e�i�V�K�X���b�h�쐬�j
	if ($in{'res'} eq "") {

		# index�t�@�C��
		local($i, $flg, $top, @new, @tmp, @top);
		open(DAT,"+< $nowfile") || &error("Open Error: $nowfile");
		eval "flock(DAT, 2);";
		$top = <DAT>;

		# �A�����eIP�`�F�b�N
		local($no,$ho,$t) = split(/<>/, $top);
		if ($host eq $ho && $wait > time - $t) {
			close(DAT);
			&error("�A�����e�͂������΂炭���Ԃ������ĉ�����");
		}
		$new = $no + 1;

		# index�W�J
		while(<DAT>) {
			local($sub,$key) = (split(/<>/))[1,6];

			$i++;

			# �X���b�h���d��
			if ($sub eq $in{'sub'}) {
				$flg++;
				last;
			} elsif ($key == 2) {
				push(@top,$_);
				next;
			}

			# �K�萔�I�[�o�[��@tmp���
			if ($i >= $i_max) {
				push(@tmp,$_);

			# �K�萔����@new���
			} else {
				push(@new,$_);
			}
		}

		# �X���b�h���d���̓G���[
		if ($flg) {
			close(DAT);
			&error("<b>�u$in{'sub'}�v</b>�͊����X���b�h�Əd�����Ă��܂��B<br>�ʂ̃X���b�h�����w�肵�Ă�������");
		}

		# �t�@�C���A�b�v
		local($upl_flg, %ex, %w ,%h);
		if ($image_upl && ($in{'upfile1'} || $in{'upfile2'} || $in{'upfile3'})) {
			require $upload;
			($ex{1},$w{1},$h{1},$ex{2},$w{2},$h{2},$ex{3},$w{3},$h{3}) = &upload($time);

			# �摜�A�b�v�̂Ƃ��̓t���O�𗧂Ă�
			if ($ex{1} || $ex{2} || $ex{3}) { $upl_flg = $time; }
		}

		# ���sindex�X�V
		unshift(@new,"$new<>$i_sub<>0<>$i_nam2<>$date<>$i_nam2<>1<>$upl_flg<>\n");
		unshift(@new,@top) if (@top > 0);
		unshift(@new,"$new<>$host<>$time<>\n");
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

		# �ߋ�index�X�V
		if (@tmp > 0) {

			$i = @tmp;
			open(DAT,"+< $pastfile") || &error("Open Error: $pastfile");
			eval "flock(DAT, 2);";
			while(<DAT>) {
				$i++;
				if ($i > $p_max) {
					local($delno) = split(/<>/);

					open(IN,"$logdir/$delno.cgi");
					my $top = <IN>;
					my $log = <IN>;
					close(IN);

					local($no,$sub,$nam,$eml,$com,$dat,$ho,$pw,$url,$mvw,$myid,$tim,$upl{1},$upl{2},$upl{3}) = split(/<>/, $log);

					# �摜�͍폜
					foreach $i (1 .. 3) {
						my ($ex,$w,$h) = split(/,/, $upl{$i});
						if ($ex) { unlink("$upldir/$tim-$i$ex"); }
					}

					unlink("$logdir/$delno.cgi");
					unlink("$logdir/$delno.dat");
					next;
				}
				push(@tmp,$_);
			}
			seek(DAT, 0, 0);
			print DAT @tmp;
			truncate(DAT, tell(DAT));
			close(DAT);
		}

		# �X���b�h�X�V
		open(OUT,"+> $logdir/$new.cgi") || &error("Write Error: $new.cgi");
		print OUT "$new<>$i_sub<>0<>1<>\n";
		print OUT "0<>$in{'sub'}<>$i_nam2<>$in{'email'}<>$i_com<>$date<>$host<>$pwd<>$in{'url'}<>$in{'mvw'}<>$my_id<>$time<>$ex{1},$w{1},$h{1}<>$ex{2},$w{2},$h{2}<>$ex{3},$w{3},$h{3}<>\n";
		close(OUT);

		# �Q�ƃt�@�C������
		open(NO,"+> $logdir/$new.dat") || &error("Write Error: $new.dat");
		print NO "0:";
		close(NO);

		# �p�[�~�b�V�����ύX
		chmod(0666, "$logdir/$new.cgi");
		chmod(0666, "$logdir/$new.dat");

		&sendmail if ($mailing);

	# �ԐM���e
	} else {

		# �Q�ƃt�@�C��
		local($data);
		open(IN,"$logdir/$in{'res'}.dat");
		$data = <IN>;
		close(IN);

		($count) = split(/:/, $data);

		# �A�����e�`�F�b�N
		local($top);
		open(IN,"$nowfile") || &error("Open Error: $nowfile");
		$top = <IN>;
		close(IN);

		local($no,$hos2,$tim2) = split(/<>/, $top);
		if ($host eq $hos2 && $wait > time - $tim2) {
			&error("�A�����e�͂������΂炭���Ԃ������ĉ�����");
		}

		# �X���b�h�ǂݍ���
		open(DAT,"+< $logdir/$in{'res'}.cgi") || &error("Open Error: $in{'res'}.cgi");
		eval "flock(DAT, 2);";
		local(@file) = <DAT>;

		# �擪�t�@�C���𒊏o�E����
		$top = shift(@file);
		local($no,$sub,$res,$key) = split(/<>/, $top);

		# ���b�N�`�F�b�N
		if ($key eq '0' || $key eq '2') {
			close(DAT);
			&error("���̃X���b�h�̓��b�N���̂��ߕԐM�ł��܂���");
		}

		# �����t�@�C���𕪉��A�d���`�F�b�N
		local($no2,$sb2,$na2,$em2,$co2) = split(/<>/, $file[$#file]);
		if ($i_nam2 eq $na2 && $i_com eq $co2) { &error("�d�����e�͋֎~�ł�"); }

		# �̔�
		$newno = $no2 + 1;

		# �L�����`�F�b�N
		if ($m_max < $res+1) { &error("�ő�L�������I�[�o�[�������ߓ��e�ł��܂���"); }
		elsif ($m_max == $res+1) { $maxflag = 1; }
		else { $maxflag = 0; }

		# �X���b�h�X�V
		$res++;
		unshift(@file,"$no<>$sub<>$res<>1<>\n");
		push(@file,"$newno<>$in{'sub'}<>$i_nam2<>$in{'email'}<>$i_com<>$date<>$host<>$pwd<>$in{'url'}<>$in{'mvw'}<>$my_id<>\n");

		seek(DAT, 0, 0);
		print DAT @file;
		truncate(DAT, tell(DAT));
		close(DAT);

		## �K��L�����I�[�o�̂Ƃ� ##
		if ($maxflag) {

			# �ߋ����Oindex�ǂݍ���
			open(BAK,"+< $pastfile") || &error("Open Error: $pastfile");
			eval "flock(BAK, 2);";
			local(@file) = <BAK>;

			# ���s���Oindex����Y���X���b�h�����o��
			local($top, @new);
			open(DAT,"+< $nowfile") || &error("Open Error: $nowfile");
			eval "flock(DAT, 2);";
			$top = <DAT>;
			while(<DAT>) {
				s/\n//;
				local($no,$sub,$re,$nam,$d,$na2,$key,$upl) = split(/<>/);

				if ($in{'res'} == $no) {
					$re++;
					unshift(@file,"$no<>$sub<>$re<>$nam<>$date<>$na2<>1<>$upl<>\n");
					next;
				}
				push(@new,"$_\n");
			}

			# ���s���Oindex�X�V
			unshift(@new,$top);
			seek(DAT, 0, 0);
			print DAT @new;
			truncate(DAT, tell(DAT));
			close(DAT);

			# �ߋ����Oindex�X�V
			seek(BAK, 0, 0);
			print BAK @file;
			truncate(BAK, tell(BAK));
			close(BAK);

		## �\�[�g���� ##
		} elsif ($in{'sort'} == 1) {

			# index�t�@�C���X�V
			local($flg, $top, @new, @top);
			open(DAT,"+< $nowfile") || &error("Open Error: $nowfile");
			eval "flock(DAT, 2);";
			$top = <DAT>;
			while(<DAT>) {
				s/\n//;
				local($no,$sub,$re,$nam,$da,$na2,$key,$upl) = split(/<>/);

				if ($key == 2) {
					push(@top,"$_\n");
					next;
				}
				if ($in{'res'} == $no) {
					$flg = 1;
					$new = "$in{'res'}<>$sub<>$res<>$nam<>$date<>$i_nam2<>1<>$upl<>\n";
					next;
				}
				push(@new,"$_\n");
			}

			if (!$flg) {
				&error("�Y���̃X���b�h��index�t�@�C���Ɍ�������܂���");
			}

			local($no2,$host2,$time2) = split(/<>/, $top);

			unshift(@new,$new);
			unshift(@new,@top) if (@top > 0);
			unshift(@new,"$no2<>$host<>$time<>\n");
			seek(DAT, 0, 0);
			print DAT @new;
			truncate(DAT, tell(DAT));
			close(DAT);

		## �\�[�g�Ȃ� ##
		} else {

			# index�t�@�C���X�V
			local($flg, $top, @new);
			open(DAT,"+< $nowfile") || &error("Open Error: $nowfile");
			eval "flock(DAT, 2);";
			$top = <DAT>;
			while(<DAT>) {
				s/\n//;
				local($no,$sub,$re,$nam,$da,$na2,$key,$upl) = split(/<>/);
				if ($in{'res'} == $no) {
					$flg = 1;
					$_ = "$in{'res'}<>$sub<>$res<>$nam<>$date<>$i_nam2<>1<>$upl<>";
				}
				push(@new,"$_\n");
			}

			if (!$flg) {
				&error("�Y���̃X���b�h��index�t�@�C���Ɍ�������܂���");
			}

			local($no2,$host2,$time2) = split(/<>/, $top);

			unshift(@new,"$no2<>$host<>$time<>\n");
			seek(DAT, 0, 0);
			print DAT @new;
			truncate(DAT, tell(DAT));
			close(DAT);
		}

		# ���[�����M
		&sendmail if ($mailing == 2);
	}

	# �N�b�L�[���i�[
	if ($in{'cook'} eq "on") {
		&set_cookie($i_nam,$in{'email'},$in{'pwd'},$in{'url'},$in{'mvw'});
	}

	# �������b�Z�[�W
	&header;
	$md = 'view';
	if ($in{'res'} eq "") { $no = $new; }
	else { $no = $in{'res'}; }

	print <<EOM;
<br><br><div align="center">
<Table border="0" cellspacing="0" cellpadding="0" width="400">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col2">
  <td bgcolor="$col2" nowrap align="center" height="60">
	<h3 style="font-size:15px">�����e���肪�Ƃ��������܂���</h3>
  </td>
</tr>
</table>
</Td></Tr></Table>
<p>
EOM

	# �ߋ����O�J��z���̏ꍇ
	if ($maxflag) {
		print "�������P�X���b�h����̍ő�L�����𒴂������߁A<br>\n";
		print "���̃X���b�h�� <a href=\"$readcgi?mode=past\">�ߋ����O</a> ";
		print "�ֈړ����܂����B\n";
		$md = 'past';
	}

	# �߂�t�H�[��
	print <<"EOM";
<table><tr><td valign="top">
<form action="$bbscgi">
<input type="submit" value="�f���֖߂�">
</form></td><td width="15"></td>
<td valign="top">
<form action="$readcgi" method="post">
<input type="hidden" name="mode" value="$md">
<input type="hidden" name="no" value="$no">
<input type="submit" value="�X���b�h������">
</form></td>
</tr>
</table>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �L���폜
#-------------------------------------------------
sub delete {
	# �����`�F�b�N
	$in{'f'}  =~ s/\D//g;
	$in{'no'} =~ s/\D//g;

	# �폜����
	if ($in{'job'} eq "del") {
		if ($in{'pwd'} eq '') { &error("�p�X���[�h�̓��̓����ł�"); }

		# �X���b�h���폜�L�����o
		local($flg,$top,$check,$last_nam,$last_dat,@new);
		open(DAT,"+< $logdir/$in{'f'}.cgi") || &error("Open Error: $in{'f'}.cgi");
		eval "flock(DAT, 2);";
		$top = <DAT>;
		while(<DAT>) {
			local($no,$sub,$nam,$eml,$com,$dat,$ho,$pw,$url,$mvw,$myid,$tim,$upl{1},$upl{2},$upl{3}) = split(/<>/);

			if ($in{'no'} == $no) {
				$flg = 1;

				# �p�X�ƍ�
				$check = &decrypt($in{'pwd'}, $pw);

				# �X���b�h�w�b�_�̃��X���𒲐�
				local($num,$sub2,$res,$key) = split(/<>/, $top);
				$res--;
				$top = "$num<>$sub2<>$res<>$key<>\n";

				# �摜�폜
				foreach $i (1 .. 3) {
					next if (!$upl{$i});

					local($ex) = split(/,/, $upl{$i});
					if (-e "$upldir/$tim-$i$ex") {
						unlink("$upldir/$tim-$i$ex");
					}
				}

				# �X�L�b�v
				next;
			}
			push(@new,$_);

			# �ŏI�L���̓��e�҂Ǝ��Ԃ��o���Ă���
			$last_nam = $nam;
			$last_dat = $dat;
		}

		if (!$flg) { &error("�Y���L������������܂���"); }
		if (!$check) { &error("�p�X���[�h���Ⴂ�܂�"); }

		# �X���b�h�X�V
		unshift(@new,$top);
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

		# index�W�J
		@new = ();
		local($top, @sort, @top);
		open(DAT,"+< $nowfile") || &error("Open Error: $nowfile");
		eval "flock(DAT, 2);";
		$top = <DAT>;
		while(<DAT>) {
			s/\n//;
			local($no,$sub,$res,$nam,$dat,$na2,$key,$upl) = split(/<>/);

			if ($key == 2) {
				push(@top,"$_\n");
				next;
			}
			if ($in{'f'} == $no) {
				# index�̃��X���𒲐����A�ŏI���e�҂Ǝ��Ԃ�u��
				$res--;
				$na2 = $last_nam;
				$dat = $last_dat;
				$_ = "$no<>$sub<>$res<>$nam<>$dat<>$na2<>$key<>$upl<>";
			}
			push(@new,"$_\n");

			# �\�[�g�p�z��
			$dat =~ s/\D//g;
			push(@sort,$dat);
		}

		# ���e���Ƀ\�[�g
		@new = @new[sort {$sort[$b] <=> $sort[$a]} 0 .. $#sort];

		# index�X�V
		unshift(@new,@top) if (@top > 0);
		unshift(@new,$top);
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

		# �������b�Z�[�W
		&header;
		print "<div align=\"center\">\n";
		print "<b>�L���͐���ɍ폜����܂����B</b>\n";
		print "<form action=\"$bbscgi\">\n";
		print "<input type=\"submit\" value=\"�f���֖߂�\"></form>\n";
		print "</div></body></html>\n";
		exit;
	}

	# �Y�����O�`�F�b�N
	local($flg,$top,$no,$sub,$nam,$eml,$com,$dat,$ho,$pw);
	open(IN,"$logdir/$in{'f'}.cgi");
	$top = <IN>;
	while(<IN>) {
		($no,$sub,$nam,$eml,$com,$dat,$ho,$pw) = split(/<>/);

		last if ($in{'no'} == $no);
	}
	close(IN);

	if ($pw eq "") {
		&error("�Y���L���̓p�X���[�h���ݒ肳��Ă��Ȃ�����<br>�폜���邱�Ƃ͂ł��܂���");
	}

	&header;
	print <<"EOM";
<div align="center">
<Table border="0" cellspacing="0" cellpadding="0" width="95%">
<Tr bgcolor="$col1"><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col3"><td bgcolor="$col3" nowrap width="92%">
<img src="$imgurl/trash.gif" align="top">
&nbsp; <b>�L���폜�t�H�[��</b></td>
<td align="right" bgcolor="$col3" nowrap>
<a href="javascript:history.back()">�O��ʂɖ߂�</a></td>
</tr></table></Td></Tr></Table>
<P>
<form action="$registcgi" method="post">
<input type="hidden" name="mode" value="del">
<input type="hidden" name="job" value="del">
<input type="hidden" name="f" value="$in{'f'}">
<input type="hidden" name="no" value="$in{'no'}">
<Table border="0" cellspacing="0" cellpadding="0" width="95%">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col2">
  <td bgcolor="$col2" width="80" nowrap>�폜�L��</td>
  <td>�L���F No.<b>$in{'no'}</b><br>�����F <b>$sub</b><br>���O�F <b>$nam</b>
  </td>
</tr>
<tr bgcolor="$col2">
  <td bgcolor="$col2" width="80" nowrap>�p�X���[�h</td>
  <td><input type="password" name="pwd" size="8" maxlength="8">
	<input type="submit" value="�L�����폜">
  </td></form>
</tr>
</table></Td></Tr></Table>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �����e����
#-------------------------------------------------
sub mente {
	# �����`�F�b�N
	$in{'f'}  =~ s/\D//g;
	$in{'no'} =~ s/\D//g;

	# �L���C��
	if ($in{'job'} eq "edit") {
		if ($in{'pwd'} eq '') { &error("�p�X���[�h�̓��̓����ł�"); }

		require $editlog;
		&edit_log("user");

	# �폜����
	} elsif ($in{'job'} eq "del") {

		if ($in{'pwd'} eq '') { &error("�p�X���[�h�̓��̓����ł�"); }

		# �X���b�h���폜�L�����o
		local($flg, $top, @new);
		open(DAT,"+< $logdir/$in{'f'}.cgi") || &error("Open Error: $in{'f'}.cgi");
		eval "flock(DAT, 2);";
		$top = <DAT>;
		while(<DAT>) {
			local($no,$sub,$nam,$eml,$com,$dat,$ho,$pw,$url,$mvw,$myid,$tim,$upl{1},$upl{2},$upl{3}) = split(/<>/);

			if ($in{'no'} == $no) {
				$flg = 1;

				# �p�X�ƍ�
				$check = &decrypt($in{'pwd'}, $pw);

				# �X���b�h�w�b�_�̃��X���𒲐�
				($num,$sub2,$res,$key) = split(/<>/, $top);
				$res--;
				$top = "$num<>$sub2<>$res<>$key<>\n";

				# �Y�t�폜
				foreach $i (1 .. 3) {
					next if (!$upl{$i});

					local($ex) = split(/,/, $upl{$i});
					if (-e "$upldir/$tim-$i$ex") {
						unlink("$upldir/$tim-$i$ex");
					}
				}

				# �X�L�b�v
				next;
			}
			push(@new,$_);

			# �ŏI�L���̓��e�҂Ǝ��Ԃ��o���Ă���
			$last_nam = $nam;
			$last_dat = $dat;
		}

		if (!$flg) { &error("�Y���L������������܂���"); }
		if (!$check) { &error("�p�X���[�h���Ⴂ�܂�"); }

		# �X���b�h�X�V
		unshift(@new,$top);
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

		# index�W�J
		@new = (); @sort = (); @top = ();
		open(DAT,"+< $nowfile") || &error("Open Error: $nowfile");
		eval "flock(DAT, 2);";
		$top = <DAT>;
		while(<DAT>) {
			s/\n//;
			local($no,$sub,$res,$nam,$dat,$na2,$key,$upl) = split(/<>/);

			if ($key == 2) {
				push(@top,"$_\n");
				next;
			}
			if ($in{'f'} == $no) {
				# index�̃��X���𒲐����A�ŏI���e�҂Ǝ��Ԃ�u��
				$res--;
				$na2 = $last_nam;
				$dat = $last_dat;
				$_ = "$no<>$sub<>$res<>$nam<>$dat<>$na2<>$key<>$upl<>";
			}
			push(@new,"$_\n");

			# �\�[�g�p�z��
			$dat =~ s/\D//g;
			push(@sort,$dat);
		}

		# ���e���Ƀ\�[�g
		@new = @new[sort {$sort[$b] <=> $sort[$a]} 0..$#sort];

		# index�X�V
		unshift(@new,@top) if (@top > 0);
		unshift(@new,$top);
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

		# �������b�Z�[�W
		&header;
		print "<div align=\"center\">\n";
		print "<b>�L���͐���ɍ폜����܂����B</b>\n";
		print "<form action=\"$bbscgi\">\n";
		print "<input type=\"submit\" value=\"�f���֖߂�\"></form>\n";
		print "</div></body></html>\n";
		exit;

	# ���b�N����
	} elsif ($in{'job'} eq "lock") {

		if ($in{'pwd'} eq '') { &error("�p�X���[�h�̓��̓����ł�"); }

		local($top);
		open(DAT,"+< $logdir/$in{'f'}.cgi") || &error("Open Error: $in{'f'}.cgi");
		eval "flock(DAT, 2);";
		local(@file) = <DAT>;

		$top = shift(@file);

		# �p�X���[�h�`�F�b�N
		local($no,$sb,$na,$em,$com,$da,$ho,$pw) = split(/<>/, $file[0]);
		if (!&decrypt($in{'pwd'}, $pw)) { &error("�p�X���[�h���Ⴂ�܂�"); }

		# �X�V
		local($num,$sub,$res,$key) = split(/<>/, $top);

		if ($key == 1) { $key = 0; }
		elsif ($key == 0) { $key = 1; }

		unshift(@file,"$num<>$sub<>$res<>$key<>\n");
		seek(DAT, 0, 0);
		print DAT @file;
		truncate(DAT, tell(DAT));
		close(DAT);

		# index�W�J
		@new = ();
		open(DAT,"+< $nowfile") || &error("Open Error: $nowfile");
		eval "flock(DAT, 2);";
		$top = <DAT>;
		while(<DAT>) {
			s/\n//;
			local($no,$sub,$res,$nam,$da,$na2,$key2,$upl) = split(/<>/);

			if ($in{'f'} == $no) {
				$_ = "$no<>$sub<>$res<>$nam<>$da<>$na2<>$key<>$upl<>";
			}
			push(@new,"$_\n");
		}

		# index�X�V
		unshift(@new,$top);
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

		# �������b�Z�[�W
		&header;
		print "<div align=\"center\">\n";

		if ($key == 1) {
			print "<b>�X���b�h�̓��b�N��������܂����B</b>\n";
		} else {
			print "<b>�X���b�h�̓��b�N����܂����B</b>\n";
		}

		print "<form action=\"$bbscgi\">\n";
		print "<input type=\"submit\" value=\"�f���֖߂�\"></form>\n";
		print "</div></body></html>\n";
		exit;
	}

	# �Y�����O�`�F�b�N
	$flg = 0;
	open(IN,"$logdir/$in{'f'}.cgi");
	$top = <IN>;
	while (<IN>) {
		($no,$sub,$name,$email,$com,$date,$host,$pw) = split(/<>/);

		last if ($in{'no'} == $no);
	}
	close(IN);

	if ($pw eq "") {
		&error("�Y���L���̓p�X���[�h���ݒ肳��Ă��܂���");
	}

	($num,$sub2,$res,$key) = split(/<>/, $top);

	&header;
	print <<"EOM";
<div align="center">
<Table border="0" cellspacing="0" cellpadding="0" width="95%">
<Tr bgcolor="$col1"><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col3"><td bgcolor="$col3" nowrap width="92%">
<img src="$imgurl/mente.gif" align="top">
&nbsp; <b>�����e�t�H�[��</b></td>
<td align="right" bgcolor="$col3" nowrap>
<a href="javascript:history.back()">�O��ʂɖ߂�</a></td>
</tr></table></Td></Tr></Table>
<P>
<form action="$registcgi" method="post">
<input type="hidden" name="mode" value="mente">
<input type="hidden" name="f" value="$in{'f'}">
<input type="hidden" name="no" value="$in{'no'}">
<Table border="0" cellspacing="0" cellpadding="0" width="95%">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col2">
  <td bgcolor="$col2" width="75" nowrap>�ΏۃX���b�h</td>
  <td>�����F <b>$sub</b><br>���O�F <b>$name</b>
  </td>
</tr>
<tr bgcolor="$col2">
  <td bgcolor="$col2" width="75" nowrap>�����I��</td>
  <td><select name="job">
	<option value="edit" selected>�L�����C��
EOM

	if ($in{'no'} eq "") {
		if ($key == 1) {
			print "<option value=\"lock\">�X���b�h�����b�N\n";
		} elsif ($key == 0) {
			print "<option value=\"lock\">���b�N������\n";
		}
	} else {
		print "<option value=\"del\">�L�����폜\n";
	}

	print <<"EOM";
	</select>
  </td>
</tr>
<tr bgcolor="$col2">
  <td bgcolor="$col2" width="75" nowrap>�p�X���[�h</td>
  <td><input type="password" name="pwd" size="10" maxlength="8">
	<input type="submit" value="���M����">
  </td></form>
</tr>
</table>
</Td></Tr></Table>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �N�b�L�[���s
#-------------------------------------------------
sub set_cookie {
	local(@cook) = @_;
	local($gmt, $cook, @t, @m, @w);

	@t = gmtime(time + 60*24*60*60);
	@m = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	@w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	# ���ەW�������`
	$gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$w[$t[6]], $t[3], $m[$t[4]], $t[5]+1900, $t[2], $t[1], $t[0]);

	# �ۑ��f�[�^��URL�G���R�[�h
	foreach (@cook) {
		s/(\W)/sprintf("%%%02X", unpack("C", $1))/eg;
		$cook .= "$_<>";
	}

	# �i�[
	print "Set-Cookie: WEB_PATIO=$cook; expires=$gmt\n";
}

#-------------------------------------------------
#  ���[�����M
#-------------------------------------------------
sub sendmail {
	local($msub, $mbody, $mcom, $email);

	# ���[���^�C�g�����`
	$msub = "$title�F $i_sub";

	# �{���̉��s�E�^�O�𕜌�
	$mcom = $i_com;
	$mcom =~ s/<br>/\n/g;
	$mcom =~ s/&lt;/��/g;
	$mcom =~ s/&gt;/��/g;
	$mcom =~ s/&quot;/�h/g;
	$mcom =~ s/&amp;/��/g;

$mbody = <<EOM;
--------------------------------------------------------
$title�Ɉȉ��̓��e������܂����B

���e�����F$date
�z�X�g���F$host
�u���E�U�F$ENV{'HTTP_USER_AGENT'}

���Ȃ܂��F$i_nam2
�d���[���F$in{'email'}
�^�C�g���F$i_sub
�t�q�k  �F$in{'url'}

$mcom
--------------------------------------------------------
EOM

	# �薼��BASE64��
	$msub = &base64($msub);

	# ���[���A�h���X���Ȃ��ꍇ�͊Ǘ��҃A�h���X�ɒu������
	if ($in{'email'} eq "") { $email = $mailto; }
	else { $email = $in{'email'}; }

	# sendmail���M
	open(MAIL,"| $sendmail -t -i") || &error("���M���s");
	print MAIL "To: $mailto\n";
	print MAIL "From: $email\n";
	print MAIL "Subject: $msub\n";
	print MAIL "MIME-Version: 1.0\n";
	print MAIL "Content-type: text/plain; charset=ISO-2022-JP\n";
	print MAIL "Content-Transfer-Encoding: 7bit\n";
	print MAIL "X-Mailer: $ver\n\n";
	foreach ( split(/\n/, $mbody) ) {
		&jcode'convert(*_, 'jis', 'sjis');
		print MAIL $_, "\n";
	}
	close(MAIL);
}

#-------------------------------------------------
#  BASE64�ϊ�
#-------------------------------------------------
#	�Ƃقق�WWW����Ō��J����Ă��郋�[�`����
#	�Q�l�ɂ��܂����B( http://tohoho.wakusei.ne.jp/ )
sub base64 {
	local($sub) = @_;
	&jcode'convert(*sub, 'jis', 'sjis');

	$sub =~ s/\x1b\x28\x42/\x1b\x28\x4a/g;
	$sub = "=?iso-2022-jp?B?" . &b64enc($sub) . "?=";
	$sub;
}
sub b64enc {
	local($ch)="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
	local($x, $y, $z, $i);
	$x = unpack("B*", $_[0]);
	for ($i=0; $y=substr($x,$i,6); $i+=6) {
		$z .= substr($ch, ord(pack("B*", "00" . $y)), 1);
		if (length($y) == 2) {
			$z .= "==";
		} elsif (length($y) == 4) {
			$z .= "=";
		}
	}
	$z;
}

#---------------------------------------
#  �g���b�v�@�\
#---------------------------------------
sub trip {
	local($name) = @_;

	$name =~ s/��/��/g;

	if ($i_nam =~ /#/) {
		local($handle,$trip) = split(/#/, $name, 2);

		local($enc) = crypt($trip, $trip_key) || crypt ($trip, '$1$' . $trip_key);
		$enc =~ s/^..//;

		return "$handle��$enc";
	} else {
		return $name;
	}
}

#-------------------------------------------------
#  �֎~���[�h�`�F�b�N
#-------------------------------------------------
sub no_wd {
	local($flg);
	foreach ( split(/,/, $no_wd) ) {
		if (index("$i_nam $i_sub $i_com",$_) >= 0) {
			$flg = 1; last;
		}
	}
	if ($flg) { &error("�֎~���[�h���܂܂�Ă��܂�"); }
}

#-------------------------------------------------
#  ���{��`�F�b�N
#-------------------------------------------------
sub jp_wd {
	local($sub, $com, $mat1, $mat2, $code1, $code2);
	$sub = $i_sub;
	$com = $i_com;

	if ($sub) {
		($mat1, $code1) = &jcode'getcode(*sub);
	}
	($mat2, $code2) = &jcode'getcode(*com);
	if ($code1 ne 'sjis' && $code2 ne 'sjis') {
		&error("�薼���̓R�����g�ɓ��{�ꂪ�܂܂�Ă��܂���");
	}
}

#-------------------------------------------------
#  URL���`�F�b�N
#-------------------------------------------------
sub urlnum {
	local($com) = $i_com;
	local($num) = ($com =~ s|(https?://)|$1|ig);
	if ($num > $urlnum) {
		&error("�R�����g����URL�A�h���X�͍ő�$urlnum�܂łł�");
	}
}


