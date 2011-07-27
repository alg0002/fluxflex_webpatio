#!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� [ WebPatio ]
#�� patio.cgi - 2011/04/08
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

# �O���t�@�C����荞��
require '../scripts/init.cgi';
require $jcode;

&parse_form;
if ($mode eq "check") {
	require $checkpl;
	&check;
}

&axscheck;
if ($mode eq "find") {
	require $findpl;
	&find;
}
elsif ($mode eq "enter_disp") { &enter_disp; }
elsif ($mode eq "logoff") { &logoff; }
&list_view;

#-------------------------------------------------
#  ���j���[���\��
#-------------------------------------------------
sub list_view {
	local($alarm,$i,$data,$top,$count);

	# �A���[������`
	$alarm = int ( $m_max * 0.9 );

	&header();
	print <<"EOM";
<div align="center">
<table width="95%" border="0">
<tr>
  <td>
	<table width="100%">
	<tr>
	<td><b style="font-size:$t_size; color:$t_color">$title</b></td>
EOM

	if ($authkey) {
		print "<td align=\"right\">�悤�����A<b>$my_name����</b></td>\n";
	}

	print <<EOM;
	</tr>
	</table>
  </td>
</tr>
<tr bgcolor="$col1">
  <td align="right" nowrap>
	<font color="$col2">|</font>
	<a href="$readcgi?mode=form"><font color="$col2">�V�K�X���b�h</font></a>
	<font color="$col2">|</font>
	<a href="$home" target="_top"><font color="$col2">�z�[���ɖ߂�</font></a>
	<font color="$col2">|</font>
	<a href="$notepage"><font color="$col2">���ӎ���</font></a>
	<font color="$col2">|</font>
	<a href="$bbscgi?mode=find"><font color="$col2">���[�h����</font></a>
	<font color="$col2">|</font>
	<a href="$readcgi?mode=past"><font color="$col2">�ߋ����O</font></a>
	<font color="$col2">|</font>
EOM

	# �F�؃��[�h�̂Ƃ�
	if ($authkey) {
		print "<a href=\"$bbscgi?mode=logoff\"><font color=\"$col2\">���O�I�t</font></a>\n";
		print "<font color=\"$col2\">|</font>\n";
	}

	print <<EOM;
	<a href="$admincgi"><font color="$col2">�Ǘ��p</font></a>
	<font color="$col2">|</font>&nbsp;&nbsp;&nbsp;
  </td>
</tr>
</table>
<p>
<Table border="0" cellspacing="0" cellpadding="0" width="95%">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col2">
  <td bgcolor="$col1"></td>
  <td bgcolor="$col1" colspan="5">
	<font color="$col2"><b>�X���b�h�ꗗ</b></font>
  </td>
</tr>
<tr bgcolor="$col2">
  <td bgcolor="$col2" width="20"><br></td>
  <td bgcolor="$col2" width="70%" nowrap><b>�g�s�b�N�X</b></td>
  <td bgcolor="$col2" nowrap><b>�쐬��</b></td>
  <td bgcolor="$col2" nowrap><b>�ԐM</b></td>
  <td bgcolor="$col2" nowrap><b>�Q��</b></td>
  <td bgcolor="$col2" nowrap><b>�ŏI�X�V</b></td></tr>
EOM

	# �X���b�h�\��
	if ($p eq "") { $p = 0; }
	$i = 0;
	open(IN,"$nowfile") || &error("Open Error: $nowfile");
	$top = <IN>;
	while (<IN>) {
		$i++;
		next if ($i < $p + 1);
		next if ($i > $p + $menu1);

		s/\n//;
		local($num,$sub,$res,$nam,$date,$na2,$key,$upl) = split(/<>/);

		# �Q�ƃJ�E���^�ǂݍ���
		open(NO,"$logdir/$num.dat");
		$data = <NO>;
		close(NO);
		($count) = split(/:/, $data);

		# �A�C�R����`
		if ($key eq '0') { $icon = 'fold3.gif'; }
		elsif ($key == 2) { $icon = 'look.gif'; }
		elsif ($res >= $alarm) { $icon = 'fold5.gif'; }
		elsif ($upl) { $icon = 'fold6.gif'; }
		else { $icon = 'fold1.gif'; }

		print "<tr bgcolor=\"$col1\"><th bgcolor=\"$col2\">";
		print "<img src=\"$imgurl/$icon\"></th>";
		print "<td bgcolor=\"$col2\" width=\"70%\">";
		print "<a href=\"$readcgi?no=$num\">$sub</a></td>";
		print "<td bgcolor=\"$col2\" nowrap>$nam</td>";
		print "<td bgcolor=\"$col2\" align=\"right\" nowrap class=\"num\">$res</td>";
		print "<td bgcolor=\"$col2\" align=\"right\" nowrap class=\"num\">$count</td>";
		print "<td bgcolor=\"$col2\" nowrap><span class=\"s1\">$date</span><br>";
		print "<span class=\"s2\">by $na2</span></td></tr>\n";
	}
	close(IN);

	print "</table></Td></Tr></Table>\n";

	# �y�[�W�ړ��{�^���\��
	if ($p - $menu1 >= 0 || $p + $menu1 < $i) {
		local($x,$y) = (1,0);
		print "<p><table width=\"95%\"><tr><td class=\"num\"> Page: ";
		while ($i > 0) {
			if ($p == $y) {
				print "<b style=\"color:$pglog_col\">$x</b> |\n";
			} else {
				print "<a href=\"$bbscgi?p=$y\">$x</a> |\n";
			}
			$x++;
			$y += $menu1;
			$i -= $menu1;
		}
		print "</td></tr></table>\n";
	}

	# ���쌠�\���i�폜�s�j
	print <<"EOM";
<br><br>
<Table border="0" cellspacing="0" cellpadding="0" width="95%">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col2"><td bgcolor="$col2" align="center">
<img src="$imgurl/fold1.gif" alt="�W���X���b�h"> �W���X���b�h &nbsp;&nbsp;
<img src="$imgurl/fold6.gif" alt="�Y�t����"> �Y�t���� &nbsp;&nbsp;
<img src="$imgurl/fold3.gif" alt="���b�N��"> ���b�N���i�����s�j&nbsp;&nbsp;
<img src="$imgurl/fold5.gif" alt="�A���[��"> �A���[���i�ԐM��$alarm���ȏ�j&nbsp;&nbsp;
<img src="$imgurl/look.gif" alt="�Ǘ��҃��b�Z�[�W"> �Ǘ��҃��b�Z�[�W
</td></tr></table></Td></Tr></Table><br><br>
<!-- ���쌠�\\�����E�폜�֎~ ($ver) -->
<span class="s1">
- <a href="http://www.kent-web.com/" target="_top">Web Patio</a> -
</span></div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  URL�G���R�[�h
#-------------------------------------------------
sub url_enc {
	local($_) = @_;

	s/(\W)/'%' . unpack('H2', $1)/eg;
	s/\s/+/g;
	$_;
}

#-------------------------------------------------
#  ���O�I�t
#-------------------------------------------------
sub logoff {
	if ($my_ckid =~ /^\w+$/) {
		unlink("$sesdir/$my_ckid.cgi");
	}
	print "Set-Cookie: patio_member=;\n";

	&enter_disp;
}

