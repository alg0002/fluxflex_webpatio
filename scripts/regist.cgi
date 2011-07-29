#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ [ WebPatio ]
#│ regist.cgi - 2011/07/06
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#│ 
#│ [ WebPatio for fluxflex]
#│ Modified by alg
#│ alg.info@gmail.com
#│ https://github.com/alg0002/fluxflex_webpatio
#└─────────────────────────────────

# 外部ファイル取り込み
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
&error("不明な処理です");

#-------------------------------------------------
#  記事投稿処理
#-------------------------------------------------
sub regist {
	local($sub,$key,$flg,$i,@top);

	# 権限チェック
	if ($authkey && $my_rank < 2) {
		&error("投稿の権限がありません$my_rank");
	}

	# POST限定
	if ($postonly && !$postflag) { &error("不正なアクセスです"); }

	# チェック
	if ($no_wd) { &no_wd; }
	if ($jp_wd) { &jp_wd; }
	if ($urlnum > 0) { &urlnum; }

	# コメント文字数チェック
	if (length($i_com) > $max_msg*2) {
		&error("文字数オーバーです。<br>全角$max_msg文字以内で記述してください");
	}

	# 汚染チェック
	$in{'res'} =~ s/\D//g;

	# 投稿内容チェック
	if ($i_com eq "") { &error("コメントの内容がありません"); }
	if ($i_nam eq "") {
		if ($in_name) { &error("名前は記入必須です"); }
		else { $i_nam = '名無しのゴンベエ'; }
	}
	if ($in_mail && $in{'email'} eq "") { &error("E-mailは記入必須です"); }
	if ($in{'email'} && $in{'email'} !~ /^[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/) {
		&error("E-mailの入力内容が不正です");
	}
	if ($i_sub eq "") { &error("タイトルは記入必須です"); }
	if ($i_sub =~ /^(\x81\x40|\s)+$/) { &error("タイトルは正しく記入してください"); }
	if ($i_nam =~ /^(\x81\x40|\s)+$/) { &error("名前は正しく記入してください"); }
	if ($i_com =~ /^(\x81\x40|\s|<br>)+$/) { &error("コメントは正しく記入してください"); }
	if ($in_pwd && $in{'pwd'} eq "") { &error("パスワードは入力必須です"); }
	if (length($in{'pwd'}) > 8) { &error("パスワードは8文字以内にして下さい"); }
	if ($in{'url'} eq "http://") { $in{'url'} = ""; }
	elsif ($in{url} && $in{url} !~ /^https?:\/\/[\w-.!~*'();\/?:\@&=+\$,%#]+$/) {
		&error("URL情報が不正です");
	}

	# 投稿キーチェック
	if ($regist_key) {
		require $regkeypl;

		if ($in{'regikey'} !~ /^\d{4}$/) {
			&error("投稿キーが入力不備です。<p>投稿フォームに戻って再読込み後、指定の数字を入力してください");
		}

		# 投稿キーチェック
		# -1 : キー不一致
		#  0 : 制限時間オーバー
		#  1 : キー一致
		local($chk) = &registkey_chk($in{'regikey'}, $in{'str_crypt'});
		if ($chk == 0) {
			&error("投稿キーが制限時間を超過しました。<p>投稿フォームに戻って再読込み後、指定の数字を再入力してください");
		} elsif ($chk == -1) {
			&error("投稿キーが不正です。<p>投稿フォームに戻って再読込み後、指定の数字を入力してください");
		}
	}

	# トリップ
	$i_nam2 = &trip($i_nam);

	# パスワード暗号化
	my $pwd;
	if ($in{'pwd'} ne "") { $pwd = &encrypt($in{'pwd'}); }

	# 新規投稿（新規スレッド作成）
	if ($in{'res'} eq "") {

		# indexファイル
		local($i, $flg, $top, @new, @tmp, @top);
		open(DAT,"+< $nowfile") || &error("Open Error: $nowfile");
		eval "flock(DAT, 2);";
		$top = <DAT>;

		# 連続投稿IPチェック
		local($no,$ho,$t) = split(/<>/, $top);
		if ($host eq $ho && $wait > time - $t) {
			close(DAT);
			&error("連続投稿はもうしばらく時間をおいて下さい");
		}
		$new = $no + 1;

		# index展開
		while(<DAT>) {
			local($sub,$key) = (split(/<>/))[1,6];

			$i++;

			# スレッド名重複
			if ($sub eq $in{'sub'}) {
				$flg++;
				last;
			} elsif ($key == 2) {
				push(@top,$_);
				next;
			}

			# 規定数オーバーは@tmp代入
			if ($i >= $i_max) {
				push(@tmp,$_);

			# 規定数内は@new代入
			} else {
				push(@new,$_);
			}
		}

		# スレッド名重複はエラー
		if ($flg) {
			close(DAT);
			&error("<b>「$in{'sub'}」</b>は既存スレッドと重複しています。<br>別のスレッド名を指定してください");
		}

		# ファイルアップ
		local($upl_flg, %ex, %w ,%h);
		if ($image_upl && ($in{'upfile1'} || $in{'upfile2'} || $in{'upfile3'})) {
			require $upload;
			($ex{1},$w{1},$h{1},$ex{2},$w{2},$h{2},$ex{3},$w{3},$h{3}) = &upload($time);

			# 画像アップのときはフラグを立てる
			if ($ex{1} || $ex{2} || $ex{3}) { $upl_flg = $time; }
		}

		# 現行index更新
		unshift(@new,"$new<>$i_sub<>0<>$i_nam2<>$date<>$i_nam2<>1<>$upl_flg<>\n");
		unshift(@new,@top) if (@top > 0);
		unshift(@new,"$new<>$host<>$time<>\n");
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

		# 過去index更新
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

					# 画像は削除
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

		# スレッド更新
		open(OUT,"+> $logdir/$new.cgi") || &error("Write Error: $new.cgi");
		print OUT "$new<>$i_sub<>0<>1<>\n";
		print OUT "0<>$in{'sub'}<>$i_nam2<>$in{'email'}<>$i_com<>$date<>$host<>$pwd<>$in{'url'}<>$in{'mvw'}<>$my_id<>$time<>$ex{1},$w{1},$h{1}<>$ex{2},$w{2},$h{2}<>$ex{3},$w{3},$h{3}<>\n";
		close(OUT);

		# 参照ファイル生成
		open(NO,"+> $logdir/$new.dat") || &error("Write Error: $new.dat");
		print NO "0:";
		close(NO);

		# パーミッション変更
		chmod(0666, "$logdir/$new.cgi");
		chmod(0666, "$logdir/$new.dat");

		&sendmail if ($mailing);

	# 返信投稿
	} else {

		# 参照ファイル
		local($data);
		open(IN,"$logdir/$in{'res'}.dat");
		$data = <IN>;
		close(IN);

		($count) = split(/:/, $data);

		# 連続投稿チェック
		local($top);
		open(IN,"$nowfile") || &error("Open Error: $nowfile");
		$top = <IN>;
		close(IN);

		local($no,$hos2,$tim2) = split(/<>/, $top);
		if ($host eq $hos2 && $wait > time - $tim2) {
			&error("連続投稿はもうしばらく時間をおいて下さい");
		}

		# スレッド読み込み
		open(DAT,"+< $logdir/$in{'res'}.cgi") || &error("Open Error: $in{'res'}.cgi");
		eval "flock(DAT, 2);";
		local(@file) = <DAT>;

		# 先頭ファイルを抽出・分解
		$top = shift(@file);
		local($no,$sub,$res,$key) = split(/<>/, $top);

		# ロックチェック
		if ($key eq '0' || $key eq '2') {
			close(DAT);
			&error("このスレッドはロック中のため返信できません");
		}

		# 末尾ファイルを分解、重複チェック
		local($no2,$sb2,$na2,$em2,$co2) = split(/<>/, $file[$#file]);
		if ($i_nam2 eq $na2 && $i_com eq $co2) { &error("重複投稿は禁止です"); }

		# 採番
		$newno = $no2 + 1;

		# 記事数チェック
		if ($m_max < $res+1) { &error("最大記事数をオーバーしたため投稿できません"); }
		elsif ($m_max == $res+1) { $maxflag = 1; }
		else { $maxflag = 0; }

		# スレッド更新
		$res++;
		unshift(@file,"$no<>$sub<>$res<>1<>\n");
		push(@file,"$newno<>$in{'sub'}<>$i_nam2<>$in{'email'}<>$i_com<>$date<>$host<>$pwd<>$in{'url'}<>$in{'mvw'}<>$my_id<>\n");

		seek(DAT, 0, 0);
		print DAT @file;
		truncate(DAT, tell(DAT));
		close(DAT);

		## 規定記事数オーバのとき ##
		if ($maxflag) {

			# 過去ログindex読み込み
			open(BAK,"+< $pastfile") || &error("Open Error: $pastfile");
			eval "flock(BAK, 2);";
			local(@file) = <BAK>;

			# 現行ログindexから該当スレッド抜き出し
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

			# 現行ログindex更新
			unshift(@new,$top);
			seek(DAT, 0, 0);
			print DAT @new;
			truncate(DAT, tell(DAT));
			close(DAT);

			# 過去ログindex更新
			seek(BAK, 0, 0);
			print BAK @file;
			truncate(BAK, tell(BAK));
			close(BAK);

		## ソートあり ##
		} elsif ($in{'sort'} == 1) {

			# indexファイル更新
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
				&error("該当のスレッドがindexファイルに見当たりません");
			}

			local($no2,$host2,$time2) = split(/<>/, $top);

			unshift(@new,$new);
			unshift(@new,@top) if (@top > 0);
			unshift(@new,"$no2<>$host<>$time<>\n");
			seek(DAT, 0, 0);
			print DAT @new;
			truncate(DAT, tell(DAT));
			close(DAT);

		## ソートなし ##
		} else {

			# indexファイル更新
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
				&error("該当のスレッドがindexファイルに見当たりません");
			}

			local($no2,$host2,$time2) = split(/<>/, $top);

			unshift(@new,"$no2<>$host<>$time<>\n");
			seek(DAT, 0, 0);
			print DAT @new;
			truncate(DAT, tell(DAT));
			close(DAT);
		}

		# メール送信
		&sendmail if ($mailing == 2);
	}

	# クッキーを格納
	if ($in{'cook'} eq "on") {
		&set_cookie($i_nam,$in{'email'},$in{'pwd'},$in{'url'},$in{'mvw'});
	}

	# 完了メッセージ
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
	<h3 style="font-size:15px">ご投稿ありがとうございました</h3>
  </td>
</tr>
</table>
</Td></Tr></Table>
<p>
EOM

	# 過去ログ繰り越しの場合
	if ($maxflag) {
		print "ただし１スレッド当りの最大記事数を超えたため、<br>\n";
		print "このスレッドは <a href=\"$readcgi?mode=past\">過去ログ</a> ";
		print "へ移動しました。\n";
		$md = 'past';
	}

	# 戻りフォーム
	print <<"EOM";
<table><tr><td valign="top">
<form action="$bbscgi">
<input type="submit" value="掲示板へ戻る">
</form></td><td width="15"></td>
<td valign="top">
<form action="$readcgi" method="post">
<input type="hidden" name="mode" value="$md">
<input type="hidden" name="no" value="$no">
<input type="submit" value="スレッドを見る">
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
#  記事削除
#-------------------------------------------------
sub delete {
	# 汚染チェック
	$in{'f'}  =~ s/\D//g;
	$in{'no'} =~ s/\D//g;

	# 削除処理
	if ($in{'job'} eq "del") {
		if ($in{'pwd'} eq '') { &error("パスワードの入力モレです"); }

		# スレッドより削除記事抽出
		local($flg,$top,$check,$last_nam,$last_dat,@new);
		open(DAT,"+< $logdir/$in{'f'}.cgi") || &error("Open Error: $in{'f'}.cgi");
		eval "flock(DAT, 2);";
		$top = <DAT>;
		while(<DAT>) {
			local($no,$sub,$nam,$eml,$com,$dat,$ho,$pw,$url,$mvw,$myid,$tim,$upl{1},$upl{2},$upl{3}) = split(/<>/);

			if ($in{'no'} == $no) {
				$flg = 1;

				# パス照合
				$check = &decrypt($in{'pwd'}, $pw);

				# スレッドヘッダのレス個数を調整
				local($num,$sub2,$res,$key) = split(/<>/, $top);
				$res--;
				$top = "$num<>$sub2<>$res<>$key<>\n";

				# 画像削除
				foreach $i (1 .. 3) {
					next if (!$upl{$i});

					local($ex) = split(/,/, $upl{$i});
					if (-e "$upldir/$tim-$i$ex") {
						unlink("$upldir/$tim-$i$ex");
					}
				}

				# スキップ
				next;
			}
			push(@new,$_);

			# 最終記事の投稿者と時間を覚えておく
			$last_nam = $nam;
			$last_dat = $dat;
		}

		if (!$flg) { &error("該当記事が見当たりません"); }
		if (!$check) { &error("パスワードが違います"); }

		# スレッド更新
		unshift(@new,$top);
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

		# index展開
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
				# indexのレス個数を調整し、最終投稿者と時間を置換
				$res--;
				$na2 = $last_nam;
				$dat = $last_dat;
				$_ = "$no<>$sub<>$res<>$nam<>$dat<>$na2<>$key<>$upl<>";
			}
			push(@new,"$_\n");

			# ソート用配列
			$dat =~ s/\D//g;
			push(@sort,$dat);
		}

		# 投稿順にソート
		@new = @new[sort {$sort[$b] <=> $sort[$a]} 0 .. $#sort];

		# index更新
		unshift(@new,@top) if (@top > 0);
		unshift(@new,$top);
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

		# 完了メッセージ
		&header;
		print "<div align=\"center\">\n";
		print "<b>記事は正常に削除されました。</b>\n";
		print "<form action=\"$bbscgi\">\n";
		print "<input type=\"submit\" value=\"掲示板へ戻る\"></form>\n";
		print "</div></body></html>\n";
		exit;
	}

	# 該当ログチェック
	local($flg,$top,$no,$sub,$nam,$eml,$com,$dat,$ho,$pw);
	open(IN,"$logdir/$in{'f'}.cgi");
	$top = <IN>;
	while(<IN>) {
		($no,$sub,$nam,$eml,$com,$dat,$ho,$pw) = split(/<>/);

		last if ($in{'no'} == $no);
	}
	close(IN);

	if ($pw eq "") {
		&error("該当記事はパスワードが設定されていないため<br>削除することはできません");
	}

	&header;
	print <<"EOM";
<div align="center">
<Table border="0" cellspacing="0" cellpadding="0" width="95%">
<Tr bgcolor="$col1"><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col3"><td bgcolor="$col3" nowrap width="92%">
<img src="$imgurl/trash.gif" align="top">
&nbsp; <b>記事削除フォーム</b></td>
<td align="right" bgcolor="$col3" nowrap>
<a href="javascript:history.back()">前画面に戻る</a></td>
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
  <td bgcolor="$col2" width="80" nowrap>削除記事</td>
  <td>記事： No.<b>$in{'no'}</b><br>件名： <b>$sub</b><br>名前： <b>$nam</b>
  </td>
</tr>
<tr bgcolor="$col2">
  <td bgcolor="$col2" width="80" nowrap>パスワード</td>
  <td><input type="password" name="pwd" size="8" maxlength="8">
	<input type="submit" value="記事を削除">
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
#  メンテ処理
#-------------------------------------------------
sub mente {
	# 汚染チェック
	$in{'f'}  =~ s/\D//g;
	$in{'no'} =~ s/\D//g;

	# 記事修正
	if ($in{'job'} eq "edit") {
		if ($in{'pwd'} eq '') { &error("パスワードの入力モレです"); }

		require $editlog;
		&edit_log("user");

	# 削除処理
	} elsif ($in{'job'} eq "del") {

		if ($in{'pwd'} eq '') { &error("パスワードの入力モレです"); }

		# スレッドより削除記事抽出
		local($flg, $top, @new);
		open(DAT,"+< $logdir/$in{'f'}.cgi") || &error("Open Error: $in{'f'}.cgi");
		eval "flock(DAT, 2);";
		$top = <DAT>;
		while(<DAT>) {
			local($no,$sub,$nam,$eml,$com,$dat,$ho,$pw,$url,$mvw,$myid,$tim,$upl{1},$upl{2},$upl{3}) = split(/<>/);

			if ($in{'no'} == $no) {
				$flg = 1;

				# パス照合
				$check = &decrypt($in{'pwd'}, $pw);

				# スレッドヘッダのレス個数を調整
				($num,$sub2,$res,$key) = split(/<>/, $top);
				$res--;
				$top = "$num<>$sub2<>$res<>$key<>\n";

				# 添付削除
				foreach $i (1 .. 3) {
					next if (!$upl{$i});

					local($ex) = split(/,/, $upl{$i});
					if (-e "$upldir/$tim-$i$ex") {
						unlink("$upldir/$tim-$i$ex");
					}
				}

				# スキップ
				next;
			}
			push(@new,$_);

			# 最終記事の投稿者と時間を覚えておく
			$last_nam = $nam;
			$last_dat = $dat;
		}

		if (!$flg) { &error("該当記事が見当たりません"); }
		if (!$check) { &error("パスワードが違います"); }

		# スレッド更新
		unshift(@new,$top);
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

		# index展開
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
				# indexのレス個数を調整し、最終投稿者と時間を置換
				$res--;
				$na2 = $last_nam;
				$dat = $last_dat;
				$_ = "$no<>$sub<>$res<>$nam<>$dat<>$na2<>$key<>$upl<>";
			}
			push(@new,"$_\n");

			# ソート用配列
			$dat =~ s/\D//g;
			push(@sort,$dat);
		}

		# 投稿順にソート
		@new = @new[sort {$sort[$b] <=> $sort[$a]} 0..$#sort];

		# index更新
		unshift(@new,@top) if (@top > 0);
		unshift(@new,$top);
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

		# 完了メッセージ
		&header;
		print "<div align=\"center\">\n";
		print "<b>記事は正常に削除されました。</b>\n";
		print "<form action=\"$bbscgi\">\n";
		print "<input type=\"submit\" value=\"掲示板へ戻る\"></form>\n";
		print "</div></body></html>\n";
		exit;

	# ロック処理
	} elsif ($in{'job'} eq "lock") {

		if ($in{'pwd'} eq '') { &error("パスワードの入力モレです"); }

		local($top);
		open(DAT,"+< $logdir/$in{'f'}.cgi") || &error("Open Error: $in{'f'}.cgi");
		eval "flock(DAT, 2);";
		local(@file) = <DAT>;

		$top = shift(@file);

		# パスワードチェック
		local($no,$sb,$na,$em,$com,$da,$ho,$pw) = split(/<>/, $file[0]);
		if (!&decrypt($in{'pwd'}, $pw)) { &error("パスワードが違います"); }

		# 更新
		local($num,$sub,$res,$key) = split(/<>/, $top);

		if ($key == 1) { $key = 0; }
		elsif ($key == 0) { $key = 1; }

		unshift(@file,"$num<>$sub<>$res<>$key<>\n");
		seek(DAT, 0, 0);
		print DAT @file;
		truncate(DAT, tell(DAT));
		close(DAT);

		# index展開
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

		# index更新
		unshift(@new,$top);
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

		# 完了メッセージ
		&header;
		print "<div align=\"center\">\n";

		if ($key == 1) {
			print "<b>スレッドはロック解除されました。</b>\n";
		} else {
			print "<b>スレッドはロックされました。</b>\n";
		}

		print "<form action=\"$bbscgi\">\n";
		print "<input type=\"submit\" value=\"掲示板へ戻る\"></form>\n";
		print "</div></body></html>\n";
		exit;
	}

	# 該当ログチェック
	$flg = 0;
	open(IN,"$logdir/$in{'f'}.cgi");
	$top = <IN>;
	while (<IN>) {
		($no,$sub,$name,$email,$com,$date,$host,$pw) = split(/<>/);

		last if ($in{'no'} == $no);
	}
	close(IN);

	if ($pw eq "") {
		&error("該当記事はパスワードが設定されていません");
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
&nbsp; <b>メンテフォーム</b></td>
<td align="right" bgcolor="$col3" nowrap>
<a href="javascript:history.back()">前画面に戻る</a></td>
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
  <td bgcolor="$col2" width="75" nowrap>対象スレッド</td>
  <td>件名： <b>$sub</b><br>名前： <b>$name</b>
  </td>
</tr>
<tr bgcolor="$col2">
  <td bgcolor="$col2" width="75" nowrap>処理選択</td>
  <td><select name="job">
	<option value="edit" selected>記事を修正
EOM

	if ($in{'no'} eq "") {
		if ($key == 1) {
			print "<option value=\"lock\">スレッドをロック\n";
		} elsif ($key == 0) {
			print "<option value=\"lock\">ロックを解除\n";
		}
	} else {
		print "<option value=\"del\">記事を削除\n";
	}

	print <<"EOM";
	</select>
  </td>
</tr>
<tr bgcolor="$col2">
  <td bgcolor="$col2" width="75" nowrap>パスワード</td>
  <td><input type="password" name="pwd" size="10" maxlength="8">
	<input type="submit" value="送信する">
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
#  クッキー発行
#-------------------------------------------------
sub set_cookie {
	local(@cook) = @_;
	local($gmt, $cook, @t, @m, @w);

	@t = gmtime(time + 60*24*60*60);
	@m = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	@w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	# 国際標準時を定義
	$gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$w[$t[6]], $t[3], $m[$t[4]], $t[5]+1900, $t[2], $t[1], $t[0]);

	# 保存データをURLエンコード
	foreach (@cook) {
		s/(\W)/sprintf("%%%02X", unpack("C", $1))/eg;
		$cook .= "$_<>";
	}

	# 格納
	print "Set-Cookie: WEB_PATIO=$cook; expires=$gmt\n";
}

#-------------------------------------------------
#  メール送信
#-------------------------------------------------
sub sendmail {
	local($msub, $mbody, $mcom, $email);

	# メールタイトルを定義
	$msub = "$title： $i_sub";

	# 本文の改行・タグを復元
	$mcom = $i_com;
	$mcom =~ s/<br>/\n/g;
	$mcom =~ s/&lt;/＜/g;
	$mcom =~ s/&gt;/＞/g;
	$mcom =~ s/&quot;/”/g;
	$mcom =~ s/&amp;/＆/g;

$mbody = <<EOM;
--------------------------------------------------------
$titleに以下の投稿がありました。

投稿日時：$date
ホスト名：$host
ブラウザ：$ENV{'HTTP_USER_AGENT'}

おなまえ：$i_nam2
Ｅメール：$in{'email'}
タイトル：$i_sub
ＵＲＬ  ：$in{'url'}

$mcom
--------------------------------------------------------
EOM

	# 題名をBASE64化
	$msub = &base64($msub);

	# メールアドレスがない場合は管理者アドレスに置き換え
	if ($in{'email'} eq "") { $email = $mailto; }
	else { $email = $in{'email'}; }

	# sendmail送信
	open(MAIL,"| $sendmail -t -i") || &error("送信失敗");
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
#  BASE64変換
#-------------------------------------------------
#	とほほのWWW入門で公開されているルーチンを
#	参考にしました。( http://tohoho.wakusei.ne.jp/ )
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
#  トリップ機能
#---------------------------------------
sub trip {
	local($name) = @_;

	$name =~ s/◆/◇/g;

	if ($i_nam =~ /#/) {
		local($handle,$trip) = split(/#/, $name, 2);

		local($enc) = crypt($trip, $trip_key) || crypt ($trip, '$1$' . $trip_key);
		$enc =~ s/^..//;

		return "$handle◆$enc";
	} else {
		return $name;
	}
}

#-------------------------------------------------
#  禁止ワードチェック
#-------------------------------------------------
sub no_wd {
	local($flg);
	foreach ( split(/,/, $no_wd) ) {
		if (index("$i_nam $i_sub $i_com",$_) >= 0) {
			$flg = 1; last;
		}
	}
	if ($flg) { &error("禁止ワードが含まれています"); }
}

#-------------------------------------------------
#  日本語チェック
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
		&error("題名又はコメントに日本語が含まれていません");
	}
}

#-------------------------------------------------
#  URL個数チェック
#-------------------------------------------------
sub urlnum {
	local($com) = $i_com;
	local($num) = ($com =~ s|(https?://)|$1|ig);
	if ($num > $urlnum) {
		&error("コメント中のURLアドレスは最大$urlnum個までです");
	}
}


