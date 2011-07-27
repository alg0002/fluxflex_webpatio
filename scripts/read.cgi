#!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� [ WebPatio ]
#�� patio.cgi - 2007/06/06
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

# �O���t�@�C����荞��
require '../scripts/init.cgi';
require $jcode;

&parse_form;
&axscheck;
if ($mode eq "form") { &form; }
elsif ($mode eq "past") { &past; }
elsif ($mode eq "view2") { &view2; }
&view;

#-------------------------------------------------
#  �X���b�h�{��
#-------------------------------------------------
sub view {
	local($no,$sub,$res,$key,$no2,$nam,$eml,$com,$dat,$ho,$pw,$url,$resub,$pno);
	local($job) = @_;

	# �A���[�����`
	local($alarm) = int ($m_max * 0.9);

	# �X�}�C���A�C�R����`
	if ($smile) {
		@s1 = split(/\s+/, $smile1);
		@s2 = split(/\s+/, $smile2);
	}

	# �����`�F�b�N
	$in{'no'} =~ s/\D//g;

	# �ߋ����O
	if ($job eq "past") {
		$bbsback = "mode=past";
		$guid = "<a href=\"$readcgi?mode=past\">�ߋ����O</a> &gt; �L���{��";

	# ���s���O
	} else {
		# �Q�Ɛ��J�E���g
		local($data);
		open(DAT,"+< $logdir/$in{'no'}.dat") || &error("Open Error: $in{'no'}.dat");
		eval "flock(DAT, 2);";
		$data = <DAT>;

		# IP����ł���΍X�V
		($count,$ip) = split(/:/, $data);
		if ($addr ne $ip) {
			$count++;
			seek(DAT, 0, 0);
			print DAT "$count:$addr";
			truncate(DAT, tell(DAT));
		}
		close(DAT);

		$bbsback = "";
		$guid = "�L���{��";
	}

	# �X���b�h�ǂݍ���
	open(IN,"$logdir/$in{'no'}.cgi") || &error("Open Error: $in{'no'}.cgi");
	$top1 = <IN>;
	$top2 = <IN>;
	chop($top2);

	($no,$sub,$res,$key) = split(/<>/, $top1);
	($no2,$sub,$nam,$eml,$com,$dat,$ho,$pw,$url,$mvw,$myid,$tim,$upl{1},$upl{2},$upl{3}) = split(/<>/, $top2);
	$com = &auto_link($com, $no);
	$resub = "Re: $sub";
	$pno = $no;

	# �A�C�R����`
	if ($job ne "past" && $key eq '0') { $icon = 'fold3.gif'; }
	elsif ($job ne "past" && $key eq '2') { $icon = 'look.gif'; }
	elsif ($job ne "past" && $res >= $alarm) { $icon = 'fold5.gif'; }
	else { $icon = 'fold1.gif'; }

	# �w�b�_
	if ($job eq "past") {
		&header($sub);
	} else {
		&header($sub, "js");
		if ($key eq '0') {
			print "<table><tr><td width=\"5%\"></td>";
			print "<td width=\"95%\"><img src=\"$imgurl/alarm.gif\"> ";
			print "���̃X���b�h��<b>���b�N</b>����Ă��܂��B";
			print "�L���̉{���݂̂ƂȂ�܂��B</td></tr></table>\n";

		} elsif ($key == 2) {
			print "<table><tr><td width=\"5%\"></td>";
			print "<td width=\"95%\"><img src=\"$imgurl/alarm.gif\"> ";
			print "���̃X���b�h��<b>�Ǘ��҂���̃��b�Z�[�W</b>�ł��B";
			print "</td></tr></table>\n";

		} elsif ($alarm <= $res) {
			print "<table><tr><td width=\"5%\"></td>";
			print "<td width=\"95%\"><img src=\"$imgurl/alarm.gif\"> ";
			print "�ԐM�L������<b>$res</b>������܂��B";
			print "<b>$m_max</b>���𒴂���Ə������݂��ł��Ȃ��Ȃ�܂��B";
			print "</td></tr></table>\n";
		}
	}

	print <<"EOM";
<div align="center">
<table width="95%"><tr><td align="right" nowrap>
<a href="$bbscgi?">�g�b�v�y�[�W</a> &gt; $guid
</td></tr></table>
<Table border="0" cellspacing="0" cellpadding="0" width="95%">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col2"><td bgcolor="$col1">
<img src="$imgurl/$icon">
<font color="$col2"><b>$sub</b></font></td></tr>
<tr bgcolor="$col1"><td bgcolor="$col2" colspan=2>
<dl>
<dt>�����F $dat
<dt>���O�F <b>$nam</b>
EOM

	if ($eml && $mvw ne '0') {
		print "&nbsp; &lt;<a href=\"mailto:$eml\" class=\"num\">$eml</a>&gt;\n";
	}
	if ($url) {
		print "<dt>�Q�ƁF <a href=\"$url\" target=\"_blank\">$url</a>\n";
	}

	print "<br><br>\n<dd>$com\n";

	local($dd_flg);
	foreach $i (1 .. 3) {
		local($ex,$w,$h) = split(/,/, $upl{$i});
		next if (!$ex);

		if (!$dd_flg) {
			print "<dd>";
			$dd_flg++;
		}

		if (defined($imgex{$ex})) {
			local($w, $h) = &resize($w, $h);
			print "<a href=\"$uplurl/$tim-$i$ex\" target=\"_blank\">";
			print "<img src=\"$uplurl/$tim-$i$ex\" align=\"top\" border=\"0\" width=\"$w\" height=\"$h\" hspace=\"3\" vspace=\"5\"></a>\n";
		} else {
			print "[<a href=\"$uplurl/$tim-$i$ex\" target=\"_blank\">$tim-$i$ex</a>]\n";
		}
	}
	print "</dl>\n";

	# �����e�{�^��
	if ($job ne "past" && $key ne '2') {
		print "<div align=\"right\">";
		print "<a href=\"$registcgi?mode=mente&f=$in{'no'}\">";
		print "<img src=\"$imgurl/mente.gif\" alt=\"�����e\" border=\"0\"></a></div>\n";
	}

	print <<EOM;
</td></tr></table>
</Td></Tr></Table>
<p>
EOM

	# �y�[�W�J�z�{�^��
	local($pglog);
	if ($p eq "") { $p = 1; }
	if ($res > 0) {
		$end = $res / $t_max;
		if ($end != int($end)) { $end++; }
	} else {
		$end=1;
	}
	if ($key != 2) {
		$pglog = &pagelink($end, $p);
		print $pglog;
	}

	if ($res > 0) {
		print "<p><Table border=\"0\" cellspacing=\"0\" cellpadding=\"0\" width=\"95%\">";
		print "<Tr><Td bgcolor=\"$col1\">";
		print "<table border=\"0\" cellspacing=\"1\" cellpadding=\"5\" width=\"100%\">\n";
	}

	# �\���͈͂��`
	$from = $res - ($t_max * $p);
	$to   = $from + $t_max;

	$i = 0;
	while (<IN>) {
		$i++;
		if ($i <= $from) { next; }
		if ($i > $to) { last; }

		chop;
		($no,$sub,$nam,$eml,$com,$dat,$ho,$pw,$url,$mvw) = split(/<>/);
		$com = &auto_link($com, $in{'no'});

		print "<tr bgcolor=\"$col1\"><td bgcolor=\"$col3\" width=\"100%\">";
		print "<img src=\"$imgurl/file.gif\"> <b>$sub</b> ";
		print "<span class=\"num\">( No.$no )</span></td>";
		print "</tr><tr bgcolor=\"$col1\"><td bgcolor=\"$col2\">\n";
		print "<dl><dt>�����F $dat<dt>���O�F <b>$nam</b>";

		if ($eml && $mvw ne '0') {
			print "&nbsp; &lt;<a href=\"mailto:$eml\" class=\"num\">$eml</a>&gt;";
		}
		if ($url) {
			print "<dt>�Q�ƁF <a href=\"$url\" target=\"_blank\">$url</a>\n";
		}
		print "<br><br>\n<dd>$com</dl>\n";

		if ($job ne "past") {
			print "<div align=\"right\">";
			print "<a href=\"$registcgi?mode=mente&f=$in{'no'}&no=$no\">";
			print "<img src=\"$imgurl/mente.gif\" alt=\"�����e\" border=\"0\"></a></div>";
		}
		print "</div></td></tr>\n";
	}
	close(IN);

	print "<tr><td><br></td></tr>" if (!$i);

	if ($res > 0) {
		print "</table></Td></Tr></Table><p>\n";
		print $pglog if ($pglog);
	}

	&form2 if ($job ne "past" && $key == 1);

	print "</div>\n</body></html>\n";
	exit;
}

#-------------------------------------------------
#  �ʋL���{��
#-------------------------------------------------
sub view2 {
	# �X�}�C���A�C�R����`
	if ($smile) {
		@s1 = split(/\s+/, $smile1);
		@s2 = split(/\s+/, $smile2);
	}

	# �����`�F�b�N
	$in{'f'}  =~ s/\D//g;

	# �L��No�F��
	if ($in{'no'} =~ /^\d+$/) { $ptn = 1; $start = $in{'no'}; }
	elsif ($in{'no'} =~ /^(\d+)\-$/) { $ptn = 2; $start = $1; }
	elsif ($in{'no'} =~ /^(\d+)\-(\d+)$/) { $ptn = 3; $start = $1; $end = $2; }
	else { &error("�L��No���s���ł�"); }

	unless (-e "$logdir/$in{'f'}\.cgi") {
		 &error("�X���b�h����������܂���");
	}

	&header($sub);
	print <<"EOM";
<div align="center">
<Table cellspacing="0" cellpadding="0" width="95%">
<Tr><Td bgcolor="$col1">
<table cellspacing="1" cellpadding="5" width="100%">
EOM

	local($flag, $top);
	open(IN,"$logdir/$in{'f'}.cgi");
	$top = <IN>;
	while (<IN>) {
		local($no,$sub,$nam,$eml,$com,$dat,$ho,$pw,$url,$mvw) = split(/<>/);
		if ($start == $no) { $flag=1; }
		if (!$flag) { next; }

		# �L���\��
		print "<tr bgcolor=\"$col1\"><td bgcolor=\"$col3\" width=\"100%\">";
		print "<img src=\"$imgurl/file.gif\"> <b>$sub</b> ";
		print "<span class=num>( No.$no )</span></td></tr>\n";
		print "<tr bgcolor=\"$col1\"><td bgcolor=\"$col2\">";
		print "<dl><dt>�����F $dat<dt>���O�F <b>$nam</b>";

		if ($eml && $mvw ne '0') {
			print "&nbsp; &lt;<a href=\"mailto:$eml\" class=\"num\">$eml</a>&gt;\n";
		}
		if ($url) {
			print "<dt>�Q�ƁF <a href=\"$url\" target=\"_blank\">$url</a>\n";
		}
		$com = &auto_link($com, $in{'f'});

		print "<br><br><dd>$com</dl><br></td></tr>\n";

		if (($ptn == 3 && $end == $no) || ($flag && $ptn == 1)) { last; }
	}
	close(IN);

	if (!$flag) {
		print "<tr bgcolor=\"$col1\"><th bgcolor=\"$col2\">";
		print "<h3>�L������������܂���</h3></th></tr>\n";
	}

	print <<"EOM";
</table></Td></Tr></Table>
<br><br>
<form>
<input type="button" value="�E�C���h�E�����" onclick="top.close();">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �V�K�t�H�[��
#-------------------------------------------------
sub form {
	# �����`�F�b�N
	if ($authkey && $my_rank < 2) {
		&error("���e�̌���������܂���");
	}

	# �w�b�_
	if ($smile) { &header("", "js"); }
	else { &header(); }

	print <<"EOM";
<div align="center">
<table width="95%">
<tr>
  <td align="right" nowrap>
	<a href="$bbscgi?">�g�b�v�y�[�W</a> &gt; �V�K�X���b�h�쐬
  </td>
</tr></table>
<Table border="0" cellspacing="0" cellpadding="0" width="95%">
<Tr bgcolor="$col1"><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col3"><td bgcolor="$col3" nowrap width="92%">
<img src="$imgurl/pen.gif" align="middle">
&nbsp; <b>�V�K�X���b�h�쐬�t�H�[��</b></td>
</tr></table></Td></Tr></Table>
EOM

	&form2("new");

	print "</div></body></html>\n";
	exit;
}

#-------------------------------------------------
#  �t�H�[�����e
#-------------------------------------------------
sub form2 {
	local($job) = @_;
	local($submit);

	# �����`�F�b�N
	if ($authkey && $my_rank < 2) {
		return;
	}

	# �N�b�L�[�擾
	local($cnam,$ceml,$cpwd,$curl,$cmvw) = &get_cookie;
	if ($curl eq "") { $curl = "http://"; }

	if ($image_upl) {
		print qq|<form action="$registcgi" method="post" name="myFORM" enctype="multipart/form-data">\n|;
	} else {
		print qq|<form action="$registcgi" method="post" name="myFORM">\n|;
	}

	print <<EOM;
<input type="hidden" name="mode" value="regist">
<Table cellspacing="0" cellpadding="0" width="95%" border="0">
<Tr><Td bgcolor="$col1">
<table cellspacing="1" cellpadding="5" width="100%" border="0">
<tr bgcolor="$col2">
  <th bgcolor="$col2" width="80">�薼</th>
  <td><input type="text" name="sub" size="30" value="$resub" maxlength="30">
EOM

	if ($job eq "new") {
		$submit = '�X���b�h�𐶐�';
	} else {
		$submit = ' �ԐM���� ';
		print "<input type=\"hidden\" name=\"res\" value=\"$in{'no'}\">\n";
		print "<input type=\"checkbox\" name=\"sort\" value=\"1\" checked>";
		print "�X���b�h���g�b�v�փ\\�[�g\n";
	}

	print <<"EOM";
  </td>
</tr>
<tr bgcolor="$col2">
  <th bgcolor="$col2" width="80">���O</th>
  <td><input type="text" name="name" size="30" value="$cnam" maxlength="20"></td>
</tr>
<tr bgcolor="$col2">
  <th bgcolor="$col2" width="80">E-Mail</th>
  <td bgcolor="$col2"><input type="text" name="email" size="30" value="$ceml">
  <select name="mvw">
EOM

	if ($cmvw eq "") { $cmvw = 1; }
	@mvw = ('��\��','�\��');
	foreach (0,1) {
		if ($cmvw == $_) {
			print "<option value=\"$_\" selected>$mvw[$_]\n";
		} else {
			print "<option value=\"$_\">$mvw[$_]\n";
		}
	}

	print <<EOM;
</select></td>
</tr>
<tr bgcolor="$col2">
  <th bgcolor="$col2" width="80">URL</th>
  <td bgcolor="$col2"><input type="text" name="url" size="45" value="$curl"></td>
</tr>
EOM

	# �V�K�X���͉摜�t�H�[��
	if ($image_upl && $job eq "new") {
		print "<tr bgcolor=\"$col2\">\n";
		print "<td bgcolor=\"$col2\" width=\"80\" align=\"center\">";
		print "<b>�摜�Y�t</b><br><span style=\"font-size:9px\">JPEG/GIF/PNG</span></td>";
		print "<td bgcolor=\"$col2\">\n";

		foreach $i (1 .. 3) {
			print "<input type=\"file\" name=\"upfile$i\" size=\"45\"><br>\n";
		}

		print "</td></tr>\n";
	}

	print <<EOM;
<tr bgcolor="$col2">
  <th bgcolor="$col2" width="80">�p�X���[�h</th>
  <td bgcolor="$col2">
  <input type="password" name="pwd" size="8" value="$cpwd" maxlength="8">
   �i�L�������e���Ɏg�p�j
  </td>
</tr>
EOM

	# ���e�L�[
	if ($regist_key) {

		# �L�[����
		require $regkeypl;
		local($str_plain,$str_crypt) = &pcp_makekey;

		# ���̓t�H�[��
		print qq |<tr bgcolor="$col2"><th bgcolor="$col2" width="80">���e�L�[</th>|;
		print qq |<td bgcolor="$col2"><input type="text" name="regikey" size="6" style="ime-mode:inactive">\n|;
		print qq |�i���e�� <img src="$registkeycgi?$str_crypt" align="absmiddle" alt="���e�L�["> ����͂��Ă��������j</td></tr>\n|;
		print qq |<input type="hidden" name="str_crypt" value="$str_crypt">\n|;
	}

	print <<EOM;
<tr bgcolor="$col2">
  <th bgcolor="$col2" width="80">�R�����g</th>
  <td bgcolor="$col2">
EOM

	# �A�C�R��
	if ($smile) {
		@s1 = split(/\s+/, $smile1);
		@s2 = split(/\s+/, $smile2);
		foreach (0 .. $#s1) {
			print "<a href=\"javascript:MyFace('$s2[$_]')\">";
			print "<img src=\"$imgurl/$s1[$_]\" border=\"0\"></a>\n";
		}
		print "<br>\n";
	}

	print <<"EOM";
<textarea name="comment" cols="48" rows="6" wrap="soft"></textarea></td></tr>
<tr bgcolor="$col2">
  <td bgcolor="$col2"><br></td>
  <td bgcolor="$col2">
    <input type="submit" value="$submit"> &nbsp;&nbsp;
    <input type="checkbox" name="cook" value="on" checked>�N�b�L�[�ۑ�</td>
  </form></tr></table>
</Td></Tr></Table>
EOM
}

#-------------------------------------------------
#  �ߋ����O�{��
#-------------------------------------------------
sub past {
	# �L���{��
	if ($in{'no'}) { &view("past");	}

	&header();
	print <<"EOM";
<div align="center">
<table width="95%"><tr><td align="right" nowrap>
<a href="$bbscgi?">�g�b�v�y�[�W</a> &gt; �ߋ����O
</td></tr></table>
<Table border="0" cellspacing="0" cellpadding="0" width="95%">
<Tr bgcolor="$col1"><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col3"><td bgcolor="$col3" nowrap width="92%">
<img src="$imgurl/memo1.gif" align="middle">
&nbsp;<b>�ߋ����O</b></td>
</tr></table></Td></Tr></Table>
<P>
<Table border="0" cellspacing="0" cellpadding="0" width="95%">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col2">
  <td bgcolor="$col2" width="16"><br></td>
  <td bgcolor="$col2" width="80%"><b>�X���b�h</b></td>
  <td bgcolor="$col2" nowrap><b>���e��</b></td>
  <td bgcolor="$col2" nowrap><b>�ԐM��</b></td>
  <td bgcolor="$col2" nowrap><b>�ŏI�X�V</b></td>
</tr>
EOM

	# �X���b�h�W�J
	local($i) = 0;
	if ($p eq "") { $p = 0; }
	open(IN,"$pastfile") || &error("Open Error: $pastfile");
	while (<IN>) {
		$i++;
		next if ($i < $p + 1);
		next if ($i > $p + $menu2);

		local($no,$sub,$res,$name,$date) = split(/<>/);

		print "<tr bgcolor=\"$col2\"><td bgcolor=\"$col2\" width=\"16\">";
		print "<img src=\"$imgurl/fold1.gif\"></td>";
		print "<td bgcolor=\"$col2\" width=\"80%\">";
		print "<a href=\"$readcgi?mode=past&no=$no\">$sub</a></td>";
		print "<td bgcolor=\"$col2\" nowrap>$name</td>";
		print "<td bgcolor=\"$col2\" align=\"right\" nowrap class=\"num\">$res</td>";
		print "<td bgcolor=\"$col2\" nowrap class=\"s1\">$date</td></tr>\n";
	}
	close(IN);

	if (!$i) {
		print "<td bgcolor=\"$col2\"></td>";
		print "<td colspan=\"4\" bgcolor=\"$col2\">- ���݉ߋ����O�͂���܂��� -</td>\n";
	}

	print "</table></Td></Tr></Table>\n";

	# �y�[�W�ړ��{�^���\��
	if ($p - $menu2 >= 0 || $p + $menu2 < $i) {
		local($x,$y) = (1,0);
		print "<p><table width=\"95%\"><tr><td class=\"num\"> Page: ";
		while ($i > 0) {
			if ($p == $y) {
				print "<b style=\"color:$pglog_col\">$x</b> |\n";
			} else {
				print "<a href=\"$readcgi?mode=past&p=$y\">$x</a> |\n";
			}
			$x++;
			$y += $menu2;
			$i -= $menu2;
		}
		print "</td></tr></table>\n";
	}

	print "</div>\n</body></html>\n";
	exit;
}


#-------------------------------------------------
#  �y�[�W�J�z�{�^��
#-------------------------------------------------
sub pagelink {
	local($end,$p) = @_;
	local($pglog);

	$pglog .= "<table width=\"95%\"><tr><td class=\"num\">Page: ";
	foreach (1 .. $end) {
		if ($p == $_) {
			$pglog .= "<b style=\"color:$pglog_col\">$_</b> |\n";
		} else {
			$pglog .= "<a href=\"$readcgi?mode=$mode&no=$pno&p=$_\">$_</a> |\n";
		}
	}
	$pglog .= "</td></tr></table>\n";
	$pglog;
}

#-------------------------------------------------
#  �����N����
#-------------------------------------------------
sub auto_link {
	local($msg, $f) = @_;

	$msg =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+)/$1<a href=\"$2\" target=\"_target\">$2<\/a>/g;
	$msg =~ s/&gt;&gt;(\d)([\d\-]*)/<a href=\"$readcgi?mode=view2&f=$f&no=$1$2\" target=\"_blank\">&gt;&gt;$1$2<\/a>/gi;

	# �X�}�C���摜�ϊ�
	if ($smile) {
		local($tmp);
		foreach (0 .. $#s1) {
			$tmp = $s2[$_];
			$tmp =~ s/([\+\*\.\?\^\$\[\-\]\|\(\)\\])/\\$1/g;
			$msg =~ s/$tmp/ <img src=\"$imgurl\/$s1[$_]\">/g;
		}
	}
	$msg;
}

#-------------------------------------------------
#  �摜���T�C�Y
#-------------------------------------------------
sub resize {
	local($w,$h) = @_;

	# �摜�\���k��
	if ($w > $img_max_w || $h > $img_max_h) {

		local($w2,$h2,$key);

		$w2 = $img_max_w / $w;
		$h2 = $img_max_h / $h;

		if ($w2 < $h2) { $key = $w2; }
		else { $key = $h2; }

		$w = int ($w * $key) || 1;
		$h = int ($h * $key) || 1;
	}
	return ($w,$h);
}

#-------------------------------------------------
#  �N�b�L�[�擾
#-------------------------------------------------
sub get_cookie {
	# �N�b�L�[���擾
	local($cook) = $ENV{'HTTP_COOKIE'};

	# �Y��ID�����o��
	local(%cook);
	foreach ( split(/;/, $cook) ) {
		local($key, $val) = split(/=/);
		$key =~ s/\s//g;

		$cook{$key} = $val;
	}

	# �f�[�^��URL�f�R�[�h���ĕ���
	local(@cook);
	foreach ( split(/<>/, $cook{'WEB_PATIO'}) ) {
		s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("H2", $1)/eg;

		push(@cook,$_);
	}
	return @cook;
}



1;

