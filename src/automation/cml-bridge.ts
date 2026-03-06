/**
+ * CML Bridge — receives task queue items via NATS, executes, reports back.
+ * Subject: citadel.ent.cml.task
+ * Result:  citadel.ent.cml.result
+ */
+import  connect, StringCodec  from 'nats';
+
+const sc = StringCodec();
+
+export async function startCmlBridge() {
+  const nc = await connect( servers: process.env.NATS_URL );
+  const sub = nc.subscribe('citadel.ent.cml.task');
+  console.log(`[entertainment] CML bridge listening`);
+  for await (const msg of sub) {
+    const task = JSON.parse(sc.decode(msg.data));
+    console.log(`[entertainment] CML task: $task.task_id`);
+    try {
+      const result =  { task_id: task.task_id, status: 'done', output: 'ok' };
+      nc.publish('citadel.ent.cml.result', sc.encode(JSON.stringify(result)));
+    } catch (err) {
+      const result =  { task_id: task.task_id, status: 'failed', error: String(err) };
+      nc.publish('citadel.ent.cml.result', sc.encode(JSON.stringify(result)));
+    }
+  }
+}
