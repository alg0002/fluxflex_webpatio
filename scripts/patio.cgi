#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ [ WebPatio ]
#│ patio.cgi - 2011/04/08
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────

# 外部ファイル取り込み
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
#  メニュー部表示
#-------------------------------------------------
sub list_view {
	local($alarm,$i,$data,$top,$count);

	# アラーム数定義
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
		print "<td align=\"right\">ようこそ、<b>$my_nameさん</b></td>\n";
	}

	print <<EOM;
	</tr>
	</table>
  </td>
</tr>
<tr bgcolor="$col1">
  <td align="right" nowrap>
	<font color="$col2">|</font>
	<a href="$readcgi?mode=form"><font color="$col2">新規スレッド</font></a>
	<font color="$col2">|</font>
	<a href="$home" target="_top"><font color="$col2">ホームに戻る</font></a>
	<font color="$col2">|</font>
	<a href="$notepage"><font color="$col2">留意事項</font></a>
	<font color="$col2">|</font>
	<a href="$bbscgi?mode=find"><font color="$col2">ワード検索</font></a>
	<font color="$col2">|</font>
	<a href="$readcgi?mode=past"><font color="$col2">過去ログ</font></a>
	<font color="$col2">|</font>
EOM

	# 認証モードのとき
	if ($authkey) {
		print "<a href=\"$bbscgi?mode=logoff\"><font color=\"$col2\">ログオフ</font></a>\n";
		print "<font color=\"$col2\">|</font>\n";
	}

	print <<EOM;
	<a href="$admincgi"><font color="$col2">管理用</font></a>
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
	<font color="$col2"><b>スレッド一覧</b></font>
  </td>
</tr>
<tr bgcolor="$col2">
  <td bgcolor="$col2" width="20"><br></td>
  <td bgcolor="$col2" width="70%" nowrap><b>トピックス</b></td>
  <td bgcolor="$col2" nowrap><b>作成者</b></td>
  <td bgcolor="$col2" nowrap><b>返信</b></td>
  <td bgcolor="$col2" nowrap><b>参照</b></td>
  <td bgcolor="$col2" nowrap><b>最終更新</b></td></tr>
EOM

	# スレッド表示
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

		# 参照カウンタ読み込み
		open(NO,"$logdir/$num.dat");
		$data = <NO>;
		close(NO);
		($count) = split(/:/, $data);

		# アイコン定義
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

	# ページ移動ボタン表示
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

	# 著作権表示（削除不可）
	print <<"EOM";
<br><br>
<Table border="0" cellspacing="0" cellpadding="0" width="95%">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col2"><td bgcolor="$col2" align="center">
<img src="$imgurl/fold1.gif" alt="標準スレッド"> 標準スレッド &nbsp;&nbsp;
<img src="$imgurl/fold6.gif" alt="添付あり"> 添付あり &nbsp;&nbsp;
<img src="$imgurl/fold3.gif" alt="ロック中"> ロック中（書込不可）&nbsp;&nbsp;
<img src="$imgurl/fold5.gif" alt="アラーム"> アラーム（返信数$alarm件以上）&nbsp;&nbsp;
<img src="$imgurl/look.gif" alt="管理者メッセージ"> 管理者メッセージ
</td></tr></table></Td></Tr></Table><br><br>
<!-- 著作権表示部・削除禁止 ($ver) -->
<span class="s1">
- <a href="http://www.kent-web.com/" target="_top">Web Patio</a> -
</span><br>
<span class="s1">
- Modified by <a href="https://github.com/alg0002/fluxflex_webpatio" target="_top">alg</a> -
</span>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  URLエンコード
#-------------------------------------------------
sub url_enc {
	local($_) = @_;

	s/(\W)/'%' . unpack('H2', $1)/eg;
	s/\s/+/g;
	$_;
}

#-------------------------------------------------
#  ログオフ
#-------------------------------------------------
sub logoff {
	if ($my_ckid =~ /^\w+$/) {
		unlink("$sesdir/$my_ckid.cgi");
	}
	print "Set-Cookie: patio_member=;\n";

	&enter_disp;
}

