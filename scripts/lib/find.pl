#��������������������������������������������������������������������
#�� [ WebPatio ]
#�� find.pl - 2007/04/09
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

#-------------------------------------------------
#  ���[�h����
#-------------------------------------------------
sub find {
	local($target,$alarm,$next,$back,$enwd,@log1,@log2,@log3,@wd);

	&header();
	print <<"EOM";
<div align="center">
<table width="95%"><tr><td align="right" nowrap>
<a href="$bbscgi?">�g�b�v�y�[�W</a> &gt; ���[�h����
</td></tr></table>
<Table border="0" cellspacing="0" cellpadding="0" width="95%">
<Tr bgcolor="$col1"><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col3"><td bgcolor="$col3" nowrap width="92%">
<img src="$imgurl/glass.gif" align="middle">
&nbsp;<b>���[�h����</b></td>
</tr></table></Td></Tr></Table>
<P>
<form action="$bbscgi" method="post">
<input type="hidden" name="mode" value="find">
<Table border="0" cellspacing="0" cellpadding="0" width="95%">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col2"><td bgcolor="$col2">
�L�[���[�h <input type="text" name="word" size="38" value="$in{'word'}"> &nbsp;
���� <select name="op">
EOM

	foreach ("AND", "OR") {
		if ($in{'op'} eq $_) {
			print "<option value=\"$_\" selected>$_\n";
		} else {
			print "<option value=\"$_\">$_\n";
		}
	}
	print "</select> &nbsp; �\\�� <select name=vw>\n";
	foreach (10,15,20,25) {
		if ($in{'vw'} == $_) {
			print "<option value=\"$_\" selected>$_��\n";
		} else {
			print "<option value=\"$_\">$_��\n";
		}
	}
	print "</select><br>�����͈� ";

	if ($in{'log'} eq "") { $in{'log'} = 0; }
	@log1 = ($nowfile, $pastfile);
	@log2 = ("���s���O", "�ߋ����O");
	@log3 = ("view", "past");
	foreach (0,1) {
		if ($in{'log'} == $_) {
			print "<input type=radio name=log value=\"$_\" checked>$log2[$_]\n";
		} else {
			print "<input type=radio name=log value=\"$_\">$log2[$_]\n";
		}
	}
	print "<br>�������� ";
	if ($in{'s'} eq "") { $in{'s'} = 1; }
	if ($in{'s'} == 1) {
		print "<input type=checkbox name=s value=\"1\" checked>�g�s�b�N�X\n";
	} else {
		print "<input type=checkbox name=s value=\"1\">�g�s�b�N�X\n";
	}
	if ($in{'n'} eq "") { $in{'n'} = 0; }
	if ($in{'n'} == 1) {
		print "<input type=checkbox name=n value=\"1\" checked>���O\n";
	} else {
		print "<input type=checkbox name=n value=\"1\">���O\n";
	}

	print <<EOM;
&nbsp;&nbsp;
<input type="submit" value="�������s">
</td></form></tr></table>
</Td></Tr></Table>
EOM

	# �������s
	if ($in{'word'} && ($in{'s'} || $in{'n'})) {

		# �A���[������`
		$alarm = int($m_max*0.9);

		print <<EOM;
<p>
<Table border="0" cellspacing="0" cellpadding="0" width="95%"><Tr>
<Td bgcolor="$col1"><table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col2"><td bgcolor="$col2" width="20"></td>
<td bgcolor="$col2" width="70%" nowrap><b>�g�s�b�N�X</b></td>
<td bgcolor="$col2" nowrap><b>�쐬��</b></td>
<td bgcolor="$col2" nowrap><b>�ԐM</b></td>
<td bgcolor="$col2" nowrap><b>�ŏI�X�V</b></td></tr>
EOM

		$in{'word'} =~ s/\x81\x40/ /g;
		@wd = split(/\s+/, $in{'word'});

		$i = 0;
		open(IN,"$log1[$in{'log'}]") || &error("Open Error: $log1[$in{'log'}]");
		$top = <IN> if (!$in{'log'});
		while (<IN>) {
			$target = '';
			local($no,$sub,$res,$nam,$date,$na2,$key,$upl) = split(/<>/);

			$target .= $sub if ($in{'s'});
			$target .= $nam if ($in{'n'});

			$flg = 0;
			foreach $wd (@wd) {
				if (index($target,$wd) >= 0) {
					$flg = 1;
					if ($in{'op'} eq 'OR') { last; }
				} else {
					if ($in{'op'} eq 'AND') { $flg = 0; last; }
				}
			}
			if ($flg) {
				$i++;
				if ($i < $p + 1) { next; }
				if ($i > $p + $in{'vw'}) { next; }

				# �A�C�R����`
				if ($key eq '0') { $icon =  'fold3.gif'; }
				elsif ($key == 2) { $icon = 'look.gif'; }
				elsif ($res >= $alarm) { $icon = 'fold5.gif'; }
				elsif ($upl) { $icon = 'fold6.gif'; }
				else { $icon = 'fold1.gif'; }

				print "<tr bgcolor=\"$col2\"><td bgcolor=\"$col2\" width=\"20\">";
				print "<img src=\"$imgurl/$icon\" alt=\"\"><br></td>";
				print "<td bgcolor=\"$col2\">";
				print "<a href=\"$readcgi?mode=$log3[$in{'log'}]&no=$no\">$sub</a></td>";
				print "<td bgcolor=\"$col2\">$nam</td>";
				print "<td bgcolor=\"$col2\" align=\"right\" class=\"num\">$res</td>";
				print "<td bgcolor=\"$col2\" nowrap><span class=\"s1\">$date</span><br>";
				print "<span class=\"s2\">by $na2</span></td></tr>\n";
			}
		}
		close(IN);

		print "<tr bgcolor=\"$col2\"><td bgcolor=\"$col2\"><br></td>";
		print "<td bgcolor=\"$col2\" colspan=\"4\">�������ʁF<b>$i</b>�� &nbsp;&nbsp;";

		$next = $p + $in{'vw'};
		$back = $p - $in{'vw'};
		$enwd = &url_enc($in{'word'});
		if ($back >= 0) {
			print "[<a href=\"$bbscgi?mode=find&p=$back&word=$enwd&vw=$in{'vw'}&op=$in{'op'}&log=$in{'log'}&s=$in{'s'}&n=$in{'n'}\">�O��$in{'vw'}��</a>]\n";
		}
		if ($next < $i) {
			print "[<a href=\"$bbscgi?mode=find&p=$next&word=$enwd&vw=$in{'vw'}&op=$in{'op'}&log=$in{'log'}&s=$in{'s'}&n=$in{'n'}\">����$in{'vw'}��</a>]\n";
		}

		print "</td></tr></table></Td></Tr></Table>\n";
	}
	print "</div>\n</body></html>\n";
	exit;
}



1;

